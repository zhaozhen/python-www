import logging;logging.basicConfig(level=logging.INFO)
from datetime import datetime
import asyncio,os,json,time
from aiohttp import web

#初始化，这是测试，当有请求是使用ｉｎｄｅｘ方法回应
def index(request):
	return web.Response(body=b'<h1>Awesome<h1>')
#一直循环loop

@asyncio.coroutine
def init(loop):
	app=web.Application(loop=loop)
	app.router.add_route('GET','/',index)
	srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
	logging.info('server started at http://127.0.0.1:9000...')
	return srv
loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

