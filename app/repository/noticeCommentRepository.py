from pprint import pprint

from app.domain.NoticeComment import NoticeComment


def deleteByNoticeId(comment):
    NoticeComment.delete(comment)


def find_by_user_id(user_id):
    info = NoticeComment.objects.aggregate(
        [
            {
                "$lookup": {
                    "from": "notice",
                    "let": {"localId": {"$toObjectId": "$notice_id"}},
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
            {"$match": {"user_id": user_id}},
        ]
    )
    # pprint(list(info))
    return list(info)


def find_by_notice_id(article_id):
    return NoticeComment.objects(notice_id=article_id)
