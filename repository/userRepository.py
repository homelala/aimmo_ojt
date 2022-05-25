from domain.User import User
from config.db import user


def save(userInfo):
    user.insert_one({"name": userInfo.name, "email": userInfo.email, "passwd": userInfo.passwd})


def findByEmail(email):
    return User.objects(email=email)


def findById(id):
    return User.objects(id=id)
