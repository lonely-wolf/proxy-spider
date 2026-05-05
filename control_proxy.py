from config import MongoClient,proxy

#保存并更新
def save_proxy(dict_proxy: dict):
    proxy.update_one(
        {"proxy_name": dict_proxy['proxy_name']},
        {"$set": dict_proxy},
        upsert = True
    )

#更新score
def update_proxy(proxy_name: str):
    proxy.update_one(
        {"proxy_name": proxy_name},
        {"$inc": {"score": 5}}
    )

def minus_proxy(proxy_name: str):
    proxy.update_one(
        {"proxy_name": proxy_name},
        {"$inc": {"score": -1}}
    )

#删除
def delete_proxy(proxy_name: str):
    proxy.delete_one({"proxy_name": proxy_name})

