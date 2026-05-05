from Config import SEARCH_URL,CURATED_URL,PHOTO_URL,THREAD,CONCURRENT,PER_PAGE,TIME_OUT,HEADERS_API,HEADERS_COMMON,KEYWORDS,logging,proxies
import asyncio
import aiohttp
import random
from save_data import save_data

#最大并发数
semaphore = asyncio.Semaphore(CONCURRENT)

class Pexelspider:
    def __init__(self,**kwargs):
        self.search_url = kwargs.get("search_url",SEARCH_URL)
        self.curated_url = kwargs.get("curated_url",CURATED_URL)

        #设置连接超时时间，若无，返回10s
        self.timeout = kwargs.get("timeout",TIME_OUT)

        #设置headers
        self.headers_api = HEADERS_API
        self.headers_common = HEADERS_COMMON

    #搜索页面爬取
    async def get_search_page(self):


        #定义异步client对象
        async with aiohttp.ClientSession(headers=self.headers_api,proxy=proxies) as session:

        #获取主体
            for kw in KEYWORDS:
                for page in range (1,81):

                    #函数控制并发量
                    async with semaphore:

                        try:
                            url = self.search_url.format(word=kw,search_page=page,per_page=PER_PAGE)
                            response = await session.get(url)
                            logging.info("search status :%s",response.status)
                            if response.status == 200:
                                data = await response.json()
                                all = data['photos']
                                for photo in all:
                                    id = photo['id']
                                    save_data(photo=photo)
                                    logging.info(f"photo is be save, id {id}")
                            #防止崩溃
                            await asyncio.sleep(random.uniform(15,20))

                        except Exception as e:
                            logging.error(f"in search error,place: {url} , reason :{e}")
    
    #推荐页面爬取
    async def get_curated_page(self):
            

        async with aiohttp.ClientSession(headers=self.headers_common) as session:

            for page in range (1,208):
                async with semaphore:
                    try:
                        url = self.curated_url.format(curated_page=page,per_page=PER_PAGE)
                        response = await session.get(url)
                        logging.info("curated status :%s",response.status)
                        data = await response.json()
                        all = data['photos']
                        for photo in all:
                            id = photo['id']
                            save_data(photo=photo)
                            logging.info(f"photo is be save, id {id}")
                        #防止崩溃
                        await asyncio.sleep(random.uniform(1.2,3.0))
                    except Exception as e:
                        logging.error(f"in curated error,place: {url} , reason:{e}")


