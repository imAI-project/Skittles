import typing
import asyncio

import websockets

from . import model


class WSDriver(model.AbsDriver):

    handler: typing.Callable[[websockets.WebSocketServerProtocol, str], typing.Any]

    task: asyncio.Task

    def __init__(self, handler: typing.Callable[[websockets.WebSocketServerProtocol, str], typing.Any]):
        self.handler = handler

    async def run(self, **kwargs):
        self.task = asyncio.create_task(self._run(**kwargs))
        return await self.task

    async def _run(self, **kwargs):
        host = kwargs.get('host', '0.0.0.0')
        port = kwargs.get('port', 8182)
        async with websockets.serve(self.handler, host, port):
            try:
                await asyncio.Future()
            except asyncio.CancelledError:
                pass

    async def kill(self):
        self.task.cancel()