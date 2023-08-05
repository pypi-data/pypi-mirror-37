import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def tcp_client():
    r, w = await asyncio.open_connection('10.0.0.1', 1337)
    w.write(bytes(2**24))
    await w.drain()
    w.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_client())
