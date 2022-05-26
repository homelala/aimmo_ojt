from config.db import noticeComment
from domain.NoticeComment import NoticeComment


def save(comment):
    NoticeComment.save(comment)


def deleteByNoticeId(noticeId):
    noticeComment.delete_one({"noticeId": noticeId})


def findByUserId(userId):
    info = noticeComment.aggregate(
        [
            {
                "$lookup": {
                    "from": "notice",
                    "let": {"localId": {"$toObjectId": "$noticeId"}},
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
            {"$match": {"userId": userId}},
        ]
    )

    return list(info)
