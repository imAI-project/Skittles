import asyncio

import quart

from . import model


class HTTPDriver(model.AbsDriver):
    
    def __init__(self, handler: callable):
        self.handler = handler

    async def run(self, **kwargs):
        app = quart.Quart(__name__)
        
        # 监听所有的 HTTP 请求
        @app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
        @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
        async def catch_all(path: str):
            req = {
                'method': quart.request.method,
                'path': path,
                'headers': quart.request.headers,
                'body': await quart.request.get_data()
            }
            resp = await self.handler(req)

            return quart.Response(
                status=resp['status'],
                headers=resp['headers'],
                response=resp['body']
            )

        # 启动 HTTP 服务
        host = kwargs.get('host', '0.0.0.0')
        port = kwargs.get('port', 8181)
        debug = kwargs.get('debug', False)

        self.loop = asyncio.get_event_loop()

        return await app.run_task(host, port, debug=debug)

    async def kill(self):
        self.loop.stop()