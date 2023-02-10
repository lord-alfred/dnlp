import asyncio
import logging

from aiohttp import web

from dnlp.helpers import sync
from dnlp.routes import routes


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)
logger = logging.getLogger(__name__)


async def get_app():
    app = web.Application(client_max_size=1024 * 1024 * 25)  # 25MB
    app.add_routes(routes)
    return app


@sync
async def serve(host: str = '0.0.0.0', port: int = 9090):
    runner = web.AppRunner(await get_app())
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info(f'Listening on {host}:{port}')
    await asyncio.Future()
