from config.db import notice
from domain.Notice import Notice
from pprint import pprint


def save(article_info):
    Notice.save(article_info)


def find_by_id(article_id):
    return Notice.objects(id=article_id)


def find_by_id_with_comment(article_id):
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


def delete_by_id(article):
    article.delete()


def update_by_id_like(article_id):
    return Notice.update()


def find_by_like_with_comment():
    info = notice.aggregate(
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
    info = notice.aggregate(
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
    info = notice.aggregate(
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
    info = notice.aggregate(
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
    info = notice.aggregate(
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
