from dto.UserCreateDto import UserCreateDto
from domain.User import User
from repository import userRepository


def userSignUp(userCreateDto):
    user = User(userCreateDto.name, userCreateDto.email, userCreateDto.passwd)
    userRepository.save(user)
    userInfo = userRepository.findByEmail(userCreateDto.email)
    print(userInfo[0]["_id"])
    return userInfo[0]["_id"]
