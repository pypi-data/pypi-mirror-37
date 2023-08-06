import asyncio
import aioredis


async def main():

    pool = await aioredis.create_pool(
        'redis://localhost')

    # async with pool.get() as conn:
    await pool.execute('set', 'my-key', 'value')

    await async_with(pool)
    await with_await(pool)
    pool.close()
    await pool.wait_closed()


async def async_with(pool):
    async with pool.get() as conn:
        value = await conn.execute('get', 'my-key')
        print('raw value:', value)


async def with_await(pool):
    # This is exactly the same as:
    #   with (yield from pool) as conn:
    with (await pool) as conn:
        value = await conn.execute('get', 'my-key')
        print('raw value:', value)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
