from flask import Flask, render_template, jsonify, request
from flask_restx import Api, Resource
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)
client = MongoClient('localhost', 27017)
db = client.PEPEROBOOKSTORE


# HTML 을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def listing():
    reviews = list(db.PEPEROBOOKSTORE.find({}, {'_id': False}))
    return jsonify({'all_articles':reviews})


# API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    nick_receive = request.form['nick_give']

    url = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=ttbrlaekgp82331907002' \
          '&QueryType=Bestseller&output=js&MaxResult=10&Version=20131101&SearchTarget=Book'
    req = requests.get(url)

    print(req.status_code)
    print(req.headers)
    print(req.text)

    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'url': url_receive,
        'comment': comment_receive,
        'nick': nick_receive

    }

    db.PEPEROBOOKSTORE.insert_one(doc)

    return jsonify({'msg': '저장이 완료되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)