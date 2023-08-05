import json
import threading

from aiohttp import web


class Monitoring:
    def __init__(self):
        pass

    async def ping(self, request):
        response = { 'message': 'pong' }
        return web.Response(text=json.dumps(response))

    def _run_api(self):
        self.app = web.Application()
        self.app.router.add_get('/ping', self.ping)
        web.run_app(self.app)

    def run_api(self):
        t = threading.Thread(target=self._run_api())
        t.daemon = True
        t.start()