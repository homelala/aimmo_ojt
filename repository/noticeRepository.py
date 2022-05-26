from bson import ObjectId

from config.db import notice
from domain.Notice import Notice


def save(article_info):
    Notice.save(article_info)


def update(article_id, title, description, tags):
    notice.update_one({"_id": article_id}, {"$set": {"title": title, "description": description, "tags": tags}})


def find_by_id(article_id):
    return Notice.objects(id=article_id)


def findByIdWithComment(article_id):
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
            {"$match": {"_id": article_id}},
        ]
    )

    return list(info)[0]


def deleteById(article_id):
    return notice.delete_one({"_id": article_id})


def updateLikeById(article_id):
    return notice.update_one({"_id": article_id}, {"$inc": {"like": 1}})


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


def finByUserId(user_id):
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
            {"$match": {"userId": user_id}},
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
