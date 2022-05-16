from bson import ObjectId

from repository import noticeRepository, userRepository
from utils.CustomException import AccessException


def registerNotice(notice):
    userInfo = userRepository.findById(ObjectId(notice.userId))
    print(userInfo[0], notice.token)
    if userInfo[0]["token"] != notice.token:
        raise AccessException("올바른 접근이 아닙니다.")
    noticeRepository.save(notice)
