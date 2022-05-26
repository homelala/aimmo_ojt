from bson import ObjectId

from repository import noticeRepository, noticeCommentRepository
from utils.CustomException import AccessException
from pprint import pprint


def register_article(article):
    if not article:
        raise AccessException("올바른 접근이 아닙니다.")
    noticeRepository.save(article)


def update_article(article_id, article_info):
    if not article_info:
        raise AccessException("올바른 접근이 아닙니다.")

    article = noticeRepository.find_by_id(ObjectId(article_id)).get()
    if article.user_id != article_info.user_id:
        raise AccessException("권한이 없는 게시물입니다.")

    article.update_info(article_info.title, article_info.description, article_info.tags)


def read_article(noticeId):
    notice = noticeRepository.find_by_id_with_comment(ObjectId(noticeId))
    return notice


def delete_article(article_id):
    noticeCommentRepository.deleteByNoticeId(ObjectId(article_id))
    article = noticeRepository.find_by_id(article_id).get()
    noticeRepository.delete_by_id(article)


def like_article(article_id, data):
    if not data:
        raise AccessException("올바른 접근이 아닙니다.")
    article = noticeRepository.find_by_id(ObjectId(article_id)).get()
    article.update_like()


def comment_article(comment):
    if not comment:
        raise AccessException("올바른 접근이 아닙니다.")
    noticeCommentRepository.save(comment)


def get_high_like_article():
    return noticeRepository.find_by_like_with_comment()


def get_high_comment_article():
    return noticeRepository.findByCountComment()


def get_recent_article():
    return noticeRepository.findByRegisterDate()


def search_article(keyword):
    return noticeRepository.find_by_title(keyword)
