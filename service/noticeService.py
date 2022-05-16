from bson import ObjectId

from repository import noticeRepository, userRepository
from utils.CustomException import AccessException


def registerNotice(notice):
    userInfo = userRepository.findById(ObjectId(notice.userId))
    if userInfo[0]["token"] != notice.token:
        raise AccessException("올바른 접근이 아닙니다.")
    noticeRepository.save(notice)


def updateNotice(notice):
    noticeInfo = noticeRepository.findById(ObjectId(notice.noticeId))
    if noticeInfo["userId"] != notice.userId:
        raise AccessException("권한이 없는 게시글입니다.")
    noticeRepository.updateNotice(ObjectId(notice.noticeId), notice.title, notice.description)


def readNotice(noticeId):
    return noticeRepository.findById(ObjectId(noticeId))


def deleteNotice(userId, noticeId):
    noticeInfo = noticeRepository.findById(ObjectId(noticeId))
    print(noticeInfo)
    if noticeInfo["userId"] != userId:
        raise AccessException("권한이 없는 게시글입니다.")
    return noticeRepository.deleteById(ObjectId(noticeId))
