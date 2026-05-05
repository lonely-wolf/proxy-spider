import logging
from pymongo import MongoClient

CONCURRENT = 20
MAX_PROXY = 1000
MIN_SCORE = 1
MAX_SCORE = 100
INIT_SCORE = 10
TIMEOUT = 33
num_max = 352
SPLIT_COUNT = 30 #多线程数

###
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close"}
###

qiyunip_url = "https://www.qiyunip.com/freeProxy/{num}.html"



#logging初始化
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s ||%(levelname)s|| %(message)s",
    encoding="utf-8"
)

#mongoDB初始化
client = MongoClient('mongodb://localhost:27017')
db = client['proxy_pool']
proxy = db['all_proxy']