import logging
from pymongo import MongoClient
import requests

#总URL
PEXEL_URL = "https://www.pexels.com/zh-cn/"


#基础数设置
THREAD = 10
CONCURRENT = 15
PER_PAGE = 80
TIME_OUT = 5

###两套headers，API利用最大化
HEADERS_API = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
    "Authorization":"w7m4oYknabR9EfzSwgV3lGQcqMqIZb6OiVoYYVMWwH8KLEyZPedSJTAl"
    "proxy"
}
HEADERS_COMMON = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}
###

KEYWORDS = [
    "nature","sky","clouds","sunset","ocean","mountain","forest","river",
    "cat","dog","bird","city","street","building","abstract","background"
]

#所有API接口和ID
SEARCH_URL = "https://api.pexels.com/v1/search?query={word}&page={search_page}&per_page={per_page}"
CURATED_URL = "https://api.pexels.com/v1/curated?page={curated_page}&per_page={per_page}"
PHOTO_URL = "https://api.pexels.com/v1/photos/{id}"


#logging日志初始化
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s ||%(levelname)s|| %(message)s ",
    encoding = "utf-8",
    filename= "pexels_spider.log",
    filemode=  "w",
)


#mongoDB初始化
client = MongoClient('mongodb://localhost:27017')
db = client['pexels_data']
pexels_data = db['all_data']

proxy = requests.get("http://127.0.0.1:5000/")
proxies = {
    "http": "http"+str(proxy.text),
    "https": "https"+str(proxy.text)
}