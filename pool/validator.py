from config import proxy,CONCURRENT,MAX_PROXY,TIMEOUT,MAX_SCORE,MIN_SCORE,logging
import time
import aiohttp
import asyncio
from control_proxy import update_proxy,delete_proxy,minus_proxy

semaphore = asyncio.Semaphore(CONCURRENT)

class Getter:
    def __init__(self):
        self.session = None
        self.semaphore = semaphore

    async def init_session(self) -> None:
        self.session = aiohttp.ClientSession()
    
    async def need_sleep(self) -> None:
            await asyncio.sleep(10)
            logging.info("db is empty, wait 10s")

    def get_element_from_db(self) -> tuple[dict ,list]:
        list_proxy = []
        while True:
            result = list(proxy.find({"status":True}))
            if result != []:
                all_proxy = {proxy['proxy_name']:proxy['score'] for proxy in result}
                logging.info("get all proxy from db")
                for i in result:
                    list_proxy.append(i['proxy_name'])
                break
            else:
                asyncio.run(self.need_sleep())
                result = list(proxy.find({"status":True}))
        return all_proxy,list_proxy
            

    ######加减分
    async def plus_score(self,proxy_name,now_score) -> None:

        if now_score <= MAX_SCORE:
            await asyncio.to_thread(update_proxy, proxy_name)
            logging.info(f"plus proxy_name: {proxy_name} , now score is {now_score+1}")
        else:
            logging.info(f"proxy_name: {proxy_name} , now score is max score {MAX_SCORE}")


    async def minus_score(self,proxy_name,now_score) -> None:
        if now_score > MIN_SCORE and now_score <= MAX_SCORE:
            await asyncio.to_thread(minus_proxy, proxy_name)
            logging.info(f"minus proxy_name: {proxy_name} , now score is {now_score-1}")
        elif now_score == MIN_SCORE:
            logging.info(f"proxy_name: {proxy_name} , now score is min score {MIN_SCORE}")
            await asyncio.to_thread(delete_proxy,proxy_name)
    ######


    async def proxy_test(self)  -> dict:
        if self.session is None:
            await self.init_session()
            all_proxy ,list_proxy= await asyncio.to_thread(self.get_element_from_db)
            for proxy_name in list_proxy:
                now_score = all_proxy[proxy_name]
                proxies = "http://"+ str(proxy_name) + ":8080"
                try:
                    async with self.semaphore:
                        response = await self.session.get(url="http://httpbin.org/delay/0.2",proxy=proxies,timeout=TIMEOUT)
                        if response.status == 200:
                            await self.plus_score(proxy_name,now_score)
                        else:
                            logging.info(f"proxy_name: {proxy_name} , test failed , status code is {response.status}")
                            await self.minus_score(proxy_name,now_score)
                except Exception as e:
                    if e == None:
                        logging.info(f"proxy_name: {proxy_name} , test failed, error is {e}")
                        await self.minus_score(proxy_name,now_score)
                    else:
                        logging.info(f"proxy_name: {proxy_name} , test failed")
                        await self.minus_score(proxy_name,now_score)
                    continue

            return all_proxy

#--------------------------------------------   
#实例化
getter = Getter()


async def validator_main():
    while True:
        all_proxy = await getter.proxy_test()
        await asyncio.sleep(60)
        return all_proxy

if __name__ == '__main__':
    all_proxy = asyncio.run(validator_main())


