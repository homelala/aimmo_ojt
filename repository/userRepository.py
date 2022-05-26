from domain.User import User
from config.db import user


def save(user):
    return user.save()


def findByEmail(email):
    return User.objects(email=email)


def findById(id):
    return User.objects(id=id)
