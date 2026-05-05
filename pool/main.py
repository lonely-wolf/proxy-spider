from proxy_catch import main
from validator import validator_main
import asyncio
from put_proxy import max_proxy

async def task1() -> None:
    await asyncio.create_task(main())

async def task2() -> None:
    asyncio.create_task(validator_main())

async def run():
    await asyncio.gather(task1(),task2())

if __name__ == '__main__':
    asyncio.run(run())
