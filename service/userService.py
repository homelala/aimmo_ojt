from dto.UserCreateDto import UserCreateDto
from domain.User import User
from repository import userRepository


def userSignUp(form: UserCreateDto):
    user = User(UserCreateDto.get__name(), UserCreateDto.get__email, UserCreateDto.get__passwd)
    userRepository.save(user)
    return user
