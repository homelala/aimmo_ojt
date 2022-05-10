from pymongo import MongoClient
import datetime

client = MongoClient(
    "127.0.0.1",
)

db = client.aimmo_ojt

collection = db.my_collection
user = db.user


# document1 = {"name": "홍길동", "bio": "한국인입니다.", "tags": ["#몽고디비", "#파이썬", "#플라스크"], "date": datetime.datetime.utcnow()}
#
# document2 = {"name": "영희", "bio": "한국인입니다.", "tags": ["#MongoDB", "#Python", "#Flask"], "date": datetime.datetime.utcnow()}
#
# L = [document1, document2]
# collection.insert_many(L)
# user.insert_one(document1)
