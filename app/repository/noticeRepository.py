from app.db import notice
from app.domain.Notice import Notice


def save(article_info):
    Notice.save(article_info)


def find_by_id(article_id):
    return Notice.objects(id=article_id)


def find_by_id_with_comment(article_id):
    info = Notice.objects.aggregate(
        [
            {"$addFields": {"notice_id": {"$toString": "$_id"}}},
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "notice_id",
                    "foreignField": "notice_id",
                    "as": "comments",
                }
            },
            {"$match": {"_id": article_id}},
        ]
    )
    return list(info)[0]


def delete_by_id(article):
    Notice.delete(article)


def find_by_like_with_comment():
    info = Notice.objects.aggregate(
        [
            {
                "$addFields": {
                    "notice_id": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "notice_id",
                    "foreignField": "notice_id",
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
    info = Notice.objects.aggregate(
        [
            {
                "$addFields": {
                    "notice_id": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "notice_id",
                    "foreignField": "notice_id",
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
    info = Notice.objects.aggregate(
        [
            {
                "$addFields": {
                    "notice_id": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "notice_id",
                    "foreignField": "notice_id",
                    "as": "comments",
                }
            },
            {
                "$addFields": {
                    "countComment": {"$size": {"$ifNull": ["$comments", []]}},
                },
            },
            {"$limit": 10},
            {"$sort": {"register_date": -1}},
        ]
    )

    return list(info)


def find_by_user_id(user_id):
    info = Notice.objects.aggregate(
        [
            {
                "$addFields": {
                    "notice_id": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "notice_id",
                    "foreignField": "notice_id",
                    "as": "comments",
                }
            },
            {
                "$addFields": {
                    "countComment": {"$size": {"$ifNull": ["$comments", []]}},
                },
            },
            {"$match": {"user_id": user_id}},
        ]
    )

    return list(info)


def find_by_title(keyword):
    info = Notice.objects.aggregate(
        [
            {
                "$addFields": {
                    "notice_id": {"$toString": "$_id"},
                },
            },
            {
                "$lookup": {
                    "from": "notice_comment",
                    "localField": "notice_id",
                    "foreignField": "notice_id",
                    "as": "comments",
                }
            },
            {"$match": {"title": {"$regex": keyword}}},
        ]
    )
    return list(info)
