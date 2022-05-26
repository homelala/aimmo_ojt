from utils.CustomException import *
from repository import noticeRepository, userRepository, noticeCommentRepository
from bson.objectid import ObjectId
from pprint import pprint


def get_my_articles(user_id, token):
    user_info = userRepository.find_by_id(ObjectId(user_id))
    if user_info[0]["token"] != token:
        raise AccessException("올바른 접근이 아닙니다.")
    notice = noticeRepository.find_by_user_id(user_id)
    return notice


def get_my_comment(user_id, token):
    user_info = userRepository.find_by_id(ObjectId(user_id))
    if user_info[0]["token"] != token:
        raise AccessException("올바른 접근이 아닙니다.")
    notice = noticeCommentRepository.find_by_user_id(user_id)
    return notice
