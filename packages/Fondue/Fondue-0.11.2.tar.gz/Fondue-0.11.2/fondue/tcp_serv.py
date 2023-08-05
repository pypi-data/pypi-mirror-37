import asyncio
import uvloop
from timeit import default_timer as timer

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def handler(r, w):
    addr = w.get_extra_info('peername')
    start = timer()
    buffer = bytearray()
    print('Connected to', addr)
    i = 0
    while True:
        data = await r.read(4096)
        if not data:
            break
        buffer += data
        i += len(data)
    diff = timer()-start
    print('Transferred:', i, 'bytes in', round(diff, 2), 'seconds', round(i / diff / 2 ** 20, 2))
    w.close()

async def main():
    server = await asyncio.start_server(handler, '', 1337)

loop = asyncio.get_event_loop()
asyncio.ensure_future(main())
loop.run_forever()
