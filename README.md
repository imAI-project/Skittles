# Skittles

> **Warning**: 本项目仍处于开发阶段，API 可能会有较大变动。

mirai-api-http Mock 测试工具。  

可以简单地将协议分为 事件（收到好友消息、收到群消息）和 命令（发送好友消息、发送群消息）两个部分。
对于客户端来说，做的事情是 ”接收事件、发送命令“，那么对于 服务端（Mock 工具）来说，做的事情就是 ”接收命令、发送事件“。

## 实现的功能

- 正向 Websocket

## 用法

```bash
pip install skittles
```

```python
import asyncio
import time
import logging
import typing

logging.basicConfig(level=logging.DEBUG)

from skittles.platform import mirai
from skittles.entity import bot, connection

bot_account = bot.Bot(
    account_id='12345678',
    nickname='bot',
    connection_types=[connection.ConnectionType.FORWARD_WS]
)  # 建立假账号，目前仅支持 websocket

mahadapter = mirai.MiraiAPIHTTPAdapter()

@mahadapter.action_handler  # 注册命令处理器
async def handler(bot: bot.Bot, connection_type: connection.ConnectionType, data: dict) -> typing.Any:
    print(bot, connection_type, data)

asyncio.run(mahadapter.run(bots=[bot_account]))
```

```python
# 发送事件
data = {
        "type": "FriendMessage",
        "sender": {"id": 1010553892, "nickname": "Rock", "remark": ""},
        "messageChain": [
            {"type": "Source", "id": 123456, "time": int(time.time())},
            {"type": "Plain", "text": "你好"},
        ],
    }

await mahadapter.emit_event(bots=[bot_account], event=data)
```

```python
await mahadapter.kill()  # 断开连接、关闭服务
```