import asyncio
import uuid
import json
import logging

import websockets

from . import model
from ..driver import model as driver_model, http, ws


class MiraiAPIHTTPAdapter(model.AbsPlatformAdapter):

    forward_http: driver_model.AbsDriver
    """正向HTTP驱动器"""

    forward_ws: driver_model.AbsDriver
    """正向WebSocket驱动器"""

    session_keys: dict
    """会话密钥"""

    handler: callable
    """消息处理器"""

    def __init__(self, handler: callable):
        self.session_keys = {}
        self.handler = handler
        
        async def ws_handler(req):
            logging.debug(req)

            if req['body'] is None: # 新连接
                session_key = str(uuid.uuid4())
                self.session_keys[session_key] = {
                    'syncId': 0,
                    'path': req['path'],
                    'websocket': req['websocket']
                }
                await self.send(
                    session_key,
                    {
                        'code': 0,
                        'session': session_key
                    },
                    ''
                )
            else: # 消息
                await self.handler(session_key, req)

        async def http_handler(req):
            # print(req)
            logging.debug(req)

        self.forward_http = http.HTTPDriver(http_handler)
        self.forward_ws = ws.WSDriver(ws_handler)

    async def run(self):
        tasks = [
            self.forward_http.run(),
            self.forward_ws.run()
        ]

        await asyncio.gather(*tasks)

    def get_session_keys(self):
        return self.session_keys.keys()
    
    async def send(self, session_key: str, data: dict, syncId: str = None):

        if syncId is None:
            syncId = str(self.session_keys[session_key]['syncId'])
            self.session_keys[session_key]['syncId'] += 1

        body = {
            'syncId': syncId,
            'data': data
        }

        logging.debug(f'>>> {session_key} {body}')

        await self.session_keys[session_key]['websocket'].send(json.dumps(body, ensure_ascii=False))
