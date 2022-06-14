from pprint import pprint

from app.db import noticeComment
from app.domain.NoticeComment import NoticeComment


def save(comment):
    NoticeComment.save(comment)


def deleteByNoticeId(comment):
    NoticeComment.delete(comment)


def find_by_user_id(user_id):
    info = NoticeComment.objects.aggregate(
        [
            {
                "$addFields": {
                    "localId": {"$toString": "$notice_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice",
                    "$let": {"foreignId": {"$toString": "_id"}},
                    # "$pipeline": [
                    #     {
                    #         "$match": {
                    #             "$expr": {"$eq": ["$$localId", "$_id"]},
                    #         }
                    #     }
                    # ],
                    "localField": "localId",
                    "foreignField": "foreignId",
                    "as": "notice",
                },
            },
            {"$match": {"user_id": user_id}},
        ]
    )
    # pprint(list(info))
    return list(info)


def find_by_notice_id(article_id):
    return NoticeComment.objects(notice_id=article_id)
