import typing

import websockets

from . import model


class WSDriver(model.AbsDriver):

    sequence = 0

    handler: typing.Callable[[websockets.WebSocketServerProtocol, str], typing.Any]
    
    def __init__(self, handler: typing.Callable[[websockets.WebSocketServerProtocol, str], typing.Any]):
        self.handler = handler

    async def run(self, **kwargs):
        host = kwargs.get('host', '0.0.0.0')
        port = kwargs.get('port', 8182)
        
        # async def handler(websocket, path):

        #     connection_id = self.sequence
        #     self.sequence += 1

        #     req = {
        #         'method': 'WS',
        #         'path': path,
        #         'headers': {},
        #         'body': None,
        #         'websocket': websocket,
        #     }
        #     await self.handler(req)

        #     async for message in websocket:
        #         req = {
        #             'method': 'WS',
        #             'path': path,
        #             'headers': {},
        #             'body': message,
        #             'websocket': websocket,
        #         }
        #         await self.handler(req)

        return await websockets.serve(self.handler, host, port)
