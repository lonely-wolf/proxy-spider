from pexels_body import Pexelspider,asyncio

async def main():
    spider = Pexelspider()  #不输则为默认值

    #创建任务1，2
    task1 = asyncio.create_task(spider.get_search_page())
    task2 = asyncio.create_task(spider.get_curated_page())

    #等待任务
    await asyncio.gather(task1,task2)


if __name__ == '__main__':
    asyncio.run(main())