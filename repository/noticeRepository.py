from config.db import notice


def save(noticeInfo):
    notice.insert_one(
        {
            "title": noticeInfo.title,
            "description": noticeInfo.description,
            "userId": noticeInfo.userId,
            "registerDate": noticeInfo.registerDate,
            "like": noticeInfo.like,
            "tags": noticeInfo.tags,
        }
    )


def updateNotice(noticeId, title, description, tags):
    notice.update_one({"_id": noticeId}, {"$set": {"title": title, "description": description, "tags": tags}})


def findById(noticeId):
    return notice.find_one({"_id": noticeId})


def deleteById(noticeId):
    return notice.delete_one({"_id": noticeId})


def updateLikeById(noticeId):
    return notice.update_one({"_id": noticeId}, {"$inc": {"like": 1}})
