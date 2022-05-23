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


def findByIdWithComment(noticeId):
    info = notice.aggregate(
        [
            {"$addFields": {"noticeId": {"$toString": "$_id"}}},
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "noticeId",
                    "foreignField": "noticeId",
                    "as": "comments",
                }
            },
            {"$match": {"_id": noticeId}},
        ]
    )

    return list(info)[0]


def deleteById(noticeId):
    return notice.delete_one({"_id": noticeId})


def updateLikeById(noticeId):
    return notice.update_one({"_id": noticeId}, {"$inc": {"like": 1}})


def findByCountLike():
    info = notice.aggregate(
        [
            {
                "$addFields": {
                    "noticeId": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "noticeId",
                    "foreignField": "noticeId",
                    "as": "comments",
                }
            },
            {
                "$addFields": {
                    "countComment": {"$size": {"$ifNull": ["$comments", []]}},
                },
            },
            {"$limit": 10},
            {"$sort": {"like": -1}},
        ]
    )

    return list(info)


def findByCountComment():
    info = notice.aggregate(
        [
            {
                "$addFields": {
                    "noticeId": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "noticeId",
                    "foreignField": "noticeId",
                    "as": "comments",
                }
            },
            {
                "$addFields": {
                    "countComment": {"$size": {"$ifNull": ["$comments", []]}},
                },
            },
            {"$limit": 10},
            {"$sort": {"countComment": -1}},
        ]
    )

    return list(info)


def findByRegisterDate():
    info = notice.aggregate(
        [
            {
                "$addFields": {
                    "noticeId": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "noticeId",
                    "foreignField": "noticeId",
                    "as": "comments",
                }
            },
            {
                "$addFields": {
                    "countComment": {"$size": {"$ifNull": ["$comments", []]}},
                },
            },
            {"$limit": 10},
            {"$sort": {"registerDate": -1}},
        ]
    )

    return list(info)


def finByUserId(userId):
    info = notice.aggregate(
        [
            {
                "$addFields": {
                    "noticeId": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "noticeId",
                    "foreignField": "noticeId",
                    "as": "comments",
                }
            },
            {
                "$addFields": {
                    "countComment": {"$size": {"$ifNull": ["$comments", []]}},
                },
            },
            {"$match": {"userId": userId}},
        ]
    )

    return list(info)


def findByTitle(keyword):
    info = notice.aggregate(
        [
            {
                "$addFields": {
                    "noticeId": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "noticeId",
                    "foreignField": "noticeId",
                    "as": "comments",
                }
            },
            {"$match": {"title": {"$regex": keyword}}},
        ]
    )
    return list(info)
