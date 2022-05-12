from config.db import user


def save(userInfo):
    user.insert_one({"name": userInfo.name, "email": userInfo.email, "passwd": userInfo.passwd})


def findByEmail(email):
    return list(user.find({"email": email}))


def findByToken(token):
    return list(user.find({"token": token}))


def updateUserToken(email, token):
    user.update_one({"email": email}, {"$set": {"token": token}})


def updateUserInfo(token, name):
    user.update_one({"token": token}, {"$set": {"name": name}})
