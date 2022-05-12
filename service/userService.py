import secrets

from utils.CustomException import *
from domain.User import User
from repository import userRepository


def userSignUp(userCreateDto):
    alreadyUserInfo = userRepository.findByEmail(userCreateDto.email)
    if alreadyUserInfo:
        raise AlreadyExistUserException("이미 존재하는 계정입니다.")
    user = User(userCreateDto.name, userCreateDto.email, userCreateDto.passwd)
    userRepository.save(user)
    userInfo = userRepository.findByEmail(userCreateDto.email)
    return userInfo[0]["_id"]


def userLogIn(userLoginDto):
    userInfo = userRepository.findByEmail(userLoginDto.email)

    if not userInfo:
        raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")
    else:
        if userInfo[0]["passwd"] != userLoginDto.passwd:
            raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")
        else:
            token = secrets.token_hex(16)
            userRepository.updateUserToken(userLoginDto.email, token)
            return userInfo[0]["_id"]


def userUpdateInfo(userUpdateInfoDto):
    userInfo = userRepository.findByToken(userUpdateInfoDto.token)
    if not userInfo:
        raise AccessException("올바른 접근이 아닙니다.")
    else:
        print(userUpdateInfoDto.name)
        userRepository.updateUserInfo(userUpdateInfoDto.token, userUpdateInfoDto.name)
