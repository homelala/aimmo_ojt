from utils.CustomException import NotExistUserException
from domain.User import User
from repository import userRepository


def userSignUp(userCreateDto):
    user = User(userCreateDto.name, userCreateDto.email, userCreateDto.passwd)
    userRepository.save(user)
    userInfo = userRepository.findByEmail(userCreateDto.email)
    print(userInfo[0]["_id"])
    return userInfo[0]["_id"]


def userLogIn(userLoginDto):
    userInfo = userRepository.findByEmail(userLoginDto.email)
    if userInfo[0] is None:
        raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")
    else:
        if userInfo[0]["passwd"] != userLoginDto.passwd:
            raise NotExistUserException("이메일 혹은 비밀번호가 틀렸습니다.")
        else:
            return userInfo[0]["_id"]
