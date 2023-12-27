import asyncio
from typing import List
import uuid
import typing
import logging
import json
import re

import websockets

from ..driver import model as driver_model, http, ws
from ..entity import bot, connection
from . import model


class MiraiAPIHTTPAdapter(model.AbsPlatformAdapter):
    
    forward_ws: ws.WSDriver
    """正向WebSocket驱动器"""

    sessions: list[dict]
    """会话列表
    [
        {
            "session_key": "uuid",
            "bot": bot.Bot,
            "connections": {
                "ws": {
                    "path": "/ws",
                    "websocket": websockets.WebSocketServerProtocol,
                }
            }
        }
    ]
    """

    verify_key: str = None

    def __init__(self):
        self.sessions = []

    async def emit_event(self, bots: List[bot.Bot], event: dict):
        for bot in bots:
            await self._ws_send(bot, event, sync_id='-1')

    async def run(self, bots: typing.List[bot.Bot], verify_key: str = None):
        """
        启动服务端，阻塞运行

        :param bots: Bot列表
        :param verify_key: 验证密钥，可选，不设置时不验证
        """
        self.verify_key = verify_key

        async def ws_handler(websocket: websockets.WebSocketServerProtocol, path: str):
            
            # 验证密钥
            verify_key = None
            if 'verifyKey' in websocket.request_headers:
                verify_key = websocket.request_headers['verifyKey']
            else:
                # 取路径中的参数: /ws?verify_key=yirimirai
                extra = re.findall(r'\?verifyKey=(.+)', path)
                if len(extra) > 0:
                    verify_key = extra[0]
            if self.verify_key is not None and verify_key != self.verify_key:
                await self._ws_send_login_msg(websocket, {
                    'code': 1,
                    'msg': '错误的verify key'
                })
                return await websocket.close()

            qq = 0
            if 'qq' in websocket.request_headers:
                qq = int(websocket.request_headers['qq'])
            else:
                # 取路径中的参数: /ws?qq=12345678
                extra = re.findall(r'\?qq=(\d+)', path)
                if len(extra) > 0:
                    qq = int(extra[0])

            bot_obj = None

            for bot in bots:
                if bot.account_id == str(qq):
                    bot_obj = bot
                    break
            if bot_obj is None:
                await self._ws_send_login_msg(websocket, {
                    'code': 1,
                    'msg': '指定的Bot不存在'
                })
                return await websocket.close()
            else:
                # 存放会话
                session_key = str(uuid.uuid4())
                self.sessions.append({
                    'session_key': session_key,
                    'bot': bot_obj,
                    'connections': {
                        'ws': {
                            'path': path,
                            'websocket': websocket
                        }
                    }
                })

                # 发送会话密钥
                await self._ws_send_login_msg(websocket, {
                    'code': 0,
                    'session': session_key
                })

                async for message in websocket:
                    if self._action_handler is None:
                        continue
                    await self._action_handler(bot_obj, connection.ConnectionType.FORWARD_WS, message)

        self.forward_ws = ws.WSDriver(ws_handler)

        return await self.forward_ws.run()

    async def _ws_send_login_msg(self, websocket: websockets.WebSocketServerProtocol, data: dict):
        return await websocket.send(json.dumps({
            'syncId': '',
            'data': data
        }, ensure_ascii=False))

    async def _ws_send(self, bot: bot.Bot, data: dict, sync_id: str = '') -> bool:
        sent = False
        for session in self.sessions:
            if session['bot'] == bot:
                await session['connections']['ws']['websocket'].send(json.dumps({
                    'syncId': sync_id,
                    'data': data
                }, ensure_ascii=False))
                sent = True
                break

        return sent

    async def send(self, bot: bot.Bot, data: dict, sync_id: str = '', connection_type: connection.ConnectionType=connection.ConnectionType.FORWARD_WS) -> bool:
        return await self._ws_send(bot, data, sync_id)

    async def kill(self):
        for session in self.sessions:
            await session['connections']['ws']['websocket'].close()

        await self.forward_ws.kill()
