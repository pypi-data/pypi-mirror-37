
import logging, threading
import requests

logging.basicConfig(level=logging.DEBUG)


import asyncio
from servant.asyncio import HttpProtocol, staticfiles, register_middleware


@pytest.fixture
def httpd():
    """
    A fixture that clears all routes and returns a new asyncio server.
    """
    # Remove all routes.  Each test needs to add its own routes.
    from servant.routing import _routes
    _routes.clear()

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    port = 8000
    server = loop.create_server(HttpProtocol, host='127.0.0.1', port=port)
    # server = loop.run_until_complete(coro)
    print('listening on port', port)
    return server


def test_404(httpd):

    server = asyncio.get_event_loop()
