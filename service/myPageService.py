from utils.CustomException import *
from repository import noticeRepository, userRepository, noticeCommentRepository
from bson.objectid import ObjectId
from pprint import pprint


def getMyNotice(userId, token):
    userInfo = userRepository.findById(ObjectId(userId))
    if userInfo[0]["token"] != token:
        raise AccessException("올바른 접근이 아닙니다.")
    notice = noticeRepository.finByUserId(userId)
    return notice


def getMyComment(userId, token):
    userInfo = userRepository.findById(ObjectId(userId))
    if userInfo[0]["token"] != token:
        raise AccessException("올바른 접근이 아닙니다.")
    notice = noticeCommentRepository.findByUserId(userId)
    return notice
