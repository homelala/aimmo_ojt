from bson import ObjectId

from repository import noticeRepository, userRepository, noticeCommentRepository
from utils.CustomException import AccessException
from pprint import pprint


def register_article(notice):
    user_info = userRepository.findById(ObjectId(notice.userId))
    if user_info[0]["token"] != notice.token:
        raise AccessException("올바른 접근이 아닙니다.")
    noticeRepository.save(notice)


def update_article(article_id, data):
    user_info = noticeRepository.findById(ObjectId(article_id))
    if user_info["userId"] != data.userId:
        raise AccessException("권한이 없는 게시글입니다.")
    noticeRepository.updateNotice(ObjectId(article_id), data.title, data.description, data.tags)


def read_article(noticeId):
    notice = noticeRepository.findByIdWithComment(ObjectId(noticeId))
    return notice


def delete_article(article_id):
    noticeCommentRepository.deleteByNoticeId(ObjectId(article_id))
    noticeRepository.deleteById(ObjectId(article_id))


def like_notice(userId, token, noticeId):
    user_info = userRepository.findById(ObjectId(userId))
    if user_info[0]["token"] != token:
        raise AccessException("올바른 접근이 아닙니다.")
    noticeRepository.updateLikeById(ObjectId(noticeId))


def comment_notice(noticeComment):
    user_info = userRepository.findById(ObjectId(noticeComment.userId))
    if user_info[0]["token"] != noticeComment.token:
        raise AccessException("올바른 접근이 아닙니다.")
    noticeCommentRepository.save(noticeComment.noticeId, noticeComment.userId, noticeComment.description, noticeComment.registerDate)


def get_high_like_notice():
    return noticeRepository.findByCountLike()


def get_high_comment_notice():
    return noticeRepository.findByCountComment()


def get_recent_notice():
    return noticeRepository.findByRegisterDate()


def search_notice(keyword):
    return noticeRepository.findByTitle(keyword)
