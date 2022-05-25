from pymongo import MongoClient

client = MongoClient(
    "127.0.0.1",
)

db = client.aimmo_ojt

user = db.User
notice = db.notice
noticeComment = db.notice_comment
