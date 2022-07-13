from bson import ObjectId

from app.repository import noticeCommentRepository, noticeRepository
from app.utils.CustomException import AccessException
from flask import g


def register_article(article):
    noticeRepository.save(article)


def update_article(article_id, article_info):

    article = noticeRepository.find_by_id(ObjectId(article_id)).get()
    if str(article.user.id) != g.user_id:
        raise AccessException("권한이 없는 게시물입니다.")

    article.update_info(article_info.title, article_info.description, article_info.tags)


def read_article(noticeId):
    notice = noticeRepository.find_by_id(ObjectId(noticeId)).get()
    return notice


def delete_article(article_id):
    comments = noticeCommentRepository.find_by_notice_id(article_id)
    for comment in comments:
        noticeCommentRepository.deleteByNoticeId(comment)
    article = noticeRepository.find_by_id(article_id).get()
    noticeRepository.delete_by_id(article)


def like_article(article_id):
    article = noticeRepository.find_by_id(ObjectId(article_id)).get()
    article.update_like()


def comment_article(comment):
    noticeCommentRepository.save(comment)


def get_high_like_article():
    return noticeRepository.find_by_like_with_comment()


def get_high_comment_article():
    return noticeRepository.findByCountComment()


def get_recent_article():
    return noticeRepository.findByRegisterDate()


def search_article(keyword):
    return noticeRepository.find_by_title(keyword)
