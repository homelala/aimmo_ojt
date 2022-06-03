from app.db import noticeComment
from app.domain.NoticeComment import NoticeComment


def save(comment):
    NoticeComment.save(comment)


def deleteByNoticeId(comment):
    NoticeComment.delete(comment)


def find_by_user_id(user_id):
    info = noticeComment.aggregate(
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
    return list(info)


def find_by_notice_id(article_id):
    return NoticeComment.objects(notice_id=article_id)
