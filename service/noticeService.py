from bson import ObjectId

from repository import noticeRepository, userRepository, noticeCommentRepository
from utils.CustomException import AccessException
from pprint import pprint


def register_article(article):
    if not article:
        raise AccessException("올바른 접근이 아닙니다.")
    print(article)
    article.save()


def update_article(article_id, data):
    user_info = noticeRepository.findById(ObjectId(article_id))
    if user_info["userId"] != data.userId:
        raise AccessException("권한이 없는 게시글입니다.")
    noticeRepository.update(ObjectId(article_id), data.title, data.description, data.tags)


def read_article(noticeId):
    notice = noticeRepository.findByIdWithComment(ObjectId(noticeId))
    return notice


def delete_article(article_id):
    noticeCommentRepository.deleteByNoticeId(ObjectId(article_id))
    noticeRepository.deleteById(ObjectId(article_id))


def like_article(notice_id, token, user_id):
    user_info = userRepository.findById(ObjectId(user_id))
    print(user_info)
    if user_info[0]["token"] != token:
        raise AccessException("올바른 접근이 아닙니다.")
    noticeRepository.updateLikeById(ObjectId(notice_id))


def comment_article(article_id, noticeComment):
    user_info = userRepository.findById(ObjectId(noticeComment.userId))
    if user_info[0]["token"] != noticeComment.token:
        raise AccessException("올바른 접근이 아닙니다.")
    noticeCommentRepository.save(article_id, noticeComment.userId, noticeComment.description, noticeComment.registerDate)


def get_high_like_article():
    return noticeRepository.findByCountLike()


def get_high_comment_article():
    return noticeRepository.findByCountComment()


def get_recent_article():
    return noticeRepository.findByRegisterDate()


def search_article(keyword):
    return noticeRepository.findByTitle(keyword)
