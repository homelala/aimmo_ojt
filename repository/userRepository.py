from config.db import user


def save(userInfo):
    user.insert_one({"name": userInfo.name, "email": userInfo.email, "passwd": userInfo.passwd})


def findByEmail(email):
    return user.find({"email": email})
