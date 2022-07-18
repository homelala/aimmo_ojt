from app.db import notice
from app.domain.notice import Notice
from pprint import pprint


def save(article_info):
    Notice.save(article_info)


def find_by_id(article_id):
    return Notice.objects(id=article_id)


def find_by_id_with_comment(article_id):
    info = Notice.objects.aggregate(
        [
            {"$addFields": {"notice_id": {"$toString": "$_id"}}},
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "notice_id",
                    "foreignField": "notice_id",
                    "as": "comments",
                }
            },
            {"$match": {"_id": article_id}},
        ]
    )
    return list(info)[0]


def delete_by_id(article):
    Notice.delete(article)
