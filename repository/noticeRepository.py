from config.db import notice


def save(noticeInfo):
    notice.insert_one({"title": noticeInfo.title, "description": noticeInfo.description, "userId": noticeInfo.userId})
