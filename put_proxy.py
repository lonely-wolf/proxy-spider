from flask import Flask
from random import choice
from config import MongoClient,proxy

def find_proxy():
    response = list(proxy.find().sort([('score',-1)]).limit(10))
    if response == None:
        return "No proxy available"
    response = choice(response)
    return response['proxy_name']



app = Flask(__name__)

@app.route('/')
def home():
    response = find_proxy()
    return response

def max_proxy():
    app.run(debug=False)

if __name__ == '__main__':
    max_proxy()