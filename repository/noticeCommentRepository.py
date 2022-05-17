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
