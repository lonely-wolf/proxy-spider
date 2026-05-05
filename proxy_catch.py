from config import CONCURRENT,HEADERS,qiyunip_url,TIMEOUT,SPLIT_COUNT,num_max,logging,INIT_SCORE,proxy,MIN_SCORE,MAX_SCORE
import asyncio
import aiohttp 
import random
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup
from control_proxy import save_proxy

semaphore = asyncio.Semaphore(CONCURRENT)
timeout = ClientTimeout(total=TIMEOUT)

class Spider_Error():
    def __init__(self):
        self.timeout = timeout
    def catch_timeerror(self,e) ->None:
        logging.error(f"request timeout,reason : {e}")
    
    def catch_serverconnctionerror(self) ->None:
        logging.error("connection has a mistake")

    def attribute_error(self) ->None:
        logging.error("can't get html")

    async def analyse_url(self,qiyunip_url,num,session) ->str:
            all_th = []
            async with semaphore:
                try:
                    response = await session.get(qiyunip_url.format(num=num),timeout=self.timeout)

                    #bs解析
                    soup = BeautifulSoup(await response.text(),"html.parser")
                    table = soup.find("table",class_="layui-table")
                    tbody = table.find("tbody")
                    trs = tbody.find_all("tr")
                    for tr in trs:
                        th = tr.find("th").get_text(strip=True)

                        logging.info(f" {response.status} , proxy_name: {th}")
                        await asyncio.sleep(random.uniform(0.5,1.5))
                        if th:
                            all_th.append(th)
                    return all_th    

                except asyncio.TimeoutError as e:
                    self.catch_timeerror(e=e)

                except Exception as e:
                    logging.error(f"get error,reason : {e}") 

class Spider(Spider_Error):
    def __init__(self,**kwargs):
        super().__init__()
        self.headers = kwargs.get("headers",{})



    def spilt_page(self) ->list:
        li = [] #装全部的li_num
        for count in range(SPLIT_COUNT):
            li_num = [] #装每一个线程包
            for num in range(1+count,num_max+1,SPLIT_COUNT):
                li_num.append(num)
            li.append(li_num)
        return li
    
    def get_mongo_proxy(self) ->dict:
        all_proxy = list(proxy.find({"status":True}))
        all_proxy = {proxy['proxy_name']:proxy['score'] for proxy in all_proxy}
        return all_proxy

    async def run_one_async(self,li_num,all_proxy) ->None:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for num in li_num:
                proxy_name = await self.analyse_url(qiyunip_url=qiyunip_url,num=num,session=session)
                if proxy_name:
                    for name in proxy_name:
                        if name:

                            #init and append score
                            if name not in all_proxy:
                                dict_proxy = {"proxy_name":name,"status":True,"score":INIT_SCORE} #str->dict
                                await asyncio.to_thread(save_proxy, dict_proxy)
                                logging.info(f"save proxy_name: {name} , give a init score of {INIT_SCORE}")
                            else:
                                continue
                        

    async def run_(self,li) ->None:
        all_proxy = self.get_mongo_proxy()
        tasks = [self.run_one_async(li_num=li_num,all_proxy=all_proxy) for li_num in li]
        results = await asyncio.gather(*tasks)
        return results

async def run():
    spider = Spider(headers=HEADERS)
    li =  spider.spilt_page()
    await spider.run_(li=li)
    return li

async def main():
        while True:
            await run()
            await asyncio.sleep(3600)


if __name__ == '__main__':
    asyncio.run(main())



    

