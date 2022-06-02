from app.utils.CustomException import *
from app.repository import userRepository
from bson.objectid import ObjectId
import jwt


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
    payload = {"email": user.email, "name": user.name}
    token = jwt.encode(payload, "secret_key", algorithm="HS256")
    user.update_token(token)
    return user


def userUpdateInfo(user):
    user_info = userRepository.find_by_id(ObjectId(user.id)).get()
    user_info.update_name(user.name)
