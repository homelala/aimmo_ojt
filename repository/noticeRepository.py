from config.db import notice


def save(noticeInfo):
    notice.insert_one(
        {
            "title": noticeInfo.title,
            "description": noticeInfo.description,
            "userId": noticeInfo.userId,
            "registerDate": noticeInfo.registerDate,
            "like": noticeInfo.like,
        }
    )


def updateNotice(noticeId, title, description):
    notice.update_one({"_id": noticeId}, {"$set": {"title": title, "description": description}})


def findById(noticeId):
    return notice.find_one({"_id": noticeId})


def deleteById(noticeId):
    print(noticeId)
    return notice.delete_one({"_id": noticeId})
