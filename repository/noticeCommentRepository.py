from config.db import noticeComment


def save(noticeId, userId, description, registerDate):
    noticeComment.insert_one(
        {
            "noticeId": noticeId,
            "userId": userId,
            "description": description,
            "registerDate": registerDate,
        }
    )


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
