from dto.UserCreateDto import UserCreateDto
from domain.User import User


def userSignUp(form: UserCreateDto):
    user = User(UserCreateDto.get__name(), UserCreateDto.get__email, UserCreateDto.get__passwd)
