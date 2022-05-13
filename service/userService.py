import secrets
import json
from schema.UserSchema import UserSchema
from utils.CustomException import *
from repository import userRepository


def userSignUp(user):
    alreadyUserInfo = userRepository.findByEmail(user.email)
    if alreadyUserInfo:
        raise AlreadyExistUserException("이미 존재하는 계정입니다.")
    userRepository.save(user)
    userInfo = userRepository.findByEmail(user.email)
    return userInfo[0]["_id"]


def userLogIn(userLoginDto):
    schema = UserSchema()
    userInfo = userRepository.findByEmail(userLoginDto.email)
    print(userInfo)
    result = schema.dump(userInfo)
    print(result)
    if not userInfo:
        raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")
    if userInfo[0]["passwd"] != userLoginDto.passwd:
        raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")
    token = secrets.token_hex(16)
    userRepository.updateUserToken(userLoginDto.email, token)
    return userInfo[0]["_id"]


def userUpdateInfo(userUpdateInfoDto):
    userInfo = userRepository.findByToken(userUpdateInfoDto.token)
    if not userInfo:
        raise AccessException("올바른 접근이 아닙니다.")
    userRepository.updateUserInfo(userUpdateInfoDto.token, userUpdateInfoDto.name)
