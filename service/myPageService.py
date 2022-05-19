import secrets
import json
from schema.UserSchema import UserSchema
from utils.CustomException import *
from repository import userRepository
from bson.objectid import ObjectId


def userSignUp(user):
    alreadyUserInfo = userRepository.findByEmail(user.email)
    if alreadyUserInfo:
        raise AlreadyExistUserException("이미 존재하는 계정입니다.")
    userRepository.save(user)
    userInfo = userRepository.findByEmail(user.email)
    return userInfo[0]["_id"]
