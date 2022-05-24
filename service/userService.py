import secrets
from utils.CustomException import *
from repository import userRepository
from bson.objectid import ObjectId


def userSignUp(user):
    print(user.email)
    alreadyUserInfo = userRepository.findByEmail(user.email)
    print(alreadyUserInfo)
    if alreadyUserInfo:
        raise AlreadyExistUserException("이미 존재하는 계정입니다.")
    userRepository.save(user)
    userInfo = userRepository.findByEmail(user.email)
    return userInfo[0]["_id"]


def userLogIn(email, passwd):
    userInfo = userRepository.findByEmail(email)
    if not userInfo:
        raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")
    if userInfo[0]["passwd"] != passwd:
        raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")
    token = secrets.token_hex(16)
    userRepository.updateUserToken(email, token)
    return userInfo[0]["_id"]


def userUpdateInfo(user):
    userInfo = userRepository.findById(ObjectId(user.id))
    if userInfo[0]["token"] != user.token:
        raise AccessException("올바른 접근이 아닙니다.")
    userRepository.updateUserInfo(ObjectId(user.id), user.name)
