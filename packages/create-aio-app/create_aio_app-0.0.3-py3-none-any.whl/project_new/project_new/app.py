from pathlib import Path
from typing import Optional, List

import aiohttp_jinja2
import aiopg.sa
from aiohttp import web
import jinja2

from project_new.routes import init_routes
from project_new.utils.common import init_config


path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    '''
    Initialize jinja2 template for application.
    '''
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )


async def init_database(app: web.Application) -> None:
    '''
    This is signal for success creating connection with database
    '''
    config = app['config']['postgres']

    engine = await aiopg.sa.create_engine(**config)
    app['db'] = engine


async def close_database(app: web.Application) -> None:
    '''
    This is signal for success closing connection with database before shutdown
    '''
    app['db'].close()
    await app['db'].wait_closed()


def init_app(config: Optional[List[str]] = None) -> web.Application:
    app = web.Application()

    init_jinja2(app)
    init_config(app, config=config)
    init_routes(app)

    app.on_startup.extend([
        init_database,
    ])
    app.on_cleanup.extend([
        close_database,
    ])

    return app
