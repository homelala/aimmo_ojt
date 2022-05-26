import secrets
from utils.CustomException import *
from repository import userRepository
from bson.objectid import ObjectId
from pprint import pprint


def userSignUp(user):
    already_user = userRepository.findByEmail(user.email)
    if already_user:
        raise AlreadyExistUserException("이미 존재하는 계정입니다.")
    user_info = userRepository.save(user)
    return user_info


def userLogIn(user, passwd):
    if not user:
        raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")
    if not user.check_passwd(passwd):
        raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")

    user.update_token(secrets.token_hex(16))
    return user


def userUpdateInfo(user):
    user_info = userRepository.find_by_id(ObjectId(user.id)).get()
    if user_info.token != user.token:
        raise AccessException("올바른 접근이 아닙니다.")
    user_info.update_name(user.name)
