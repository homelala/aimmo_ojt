from pprint import pprint

from app.domain.notice_comment import NoticeComment


def deleteByNoticeId(comment):
    NoticeComment.delete(comment)


def find_by_notice_id(article_id):
    return NoticeComment.objects(notice_id=article_id)
