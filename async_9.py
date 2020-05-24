# вариант асинхронного скачивания файлов.

import asyncio
import requests
import aiohttp  # http запросы на сервер
from time import time


# url = 'https://loremflickr.com/320/240'

async def get_content(url, session):
    async with session.get(url, allow_redirects=True) as responce:
        data = await responce.read()
        write_file(data)


def write_file(data):
    filename = 'file - {}.jpeg'.format(int(time()*1000))
    with open(filename, 'wb', ) as file:
        file.write(data)


async def main():
    t0 = time()

    url = 'https://loremflickr.com/320/240'
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(get_content(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)

    print(time() - t0)


if __name__ == '__main__':
    asyncio.run(main())
