from pprint import pprint

from config.db import noticeComment
from domain.NoticeComment import NoticeComment


def save(comment):
    NoticeComment.save(comment)


def deleteByNoticeId(noticeId):
    noticeComment.delete_one({"noticeId": noticeId})


def find_by_user_id(user_id):
    info = noticeComment.aggregate(
        [
            {
                "$lookup": {
                    "from": "notice",
                    "let": {"localId": {"$toObjectId": "$notice_id"}},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$$localId", "$_id"]},
                            }
                        }
                    ],
                    "as": "notice",
                }
            },
            {"$match": {"user_id": user_id}},
        ]
    )
    return list(info)
