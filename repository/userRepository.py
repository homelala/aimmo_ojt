from config.db import user


def save(userInfo):
    print(userInfo)
    user.insert_one({"name": userInfo.name, "email": userInfo.email, "passwd": userInfo.passwd})


def findByEmail(email):
    return list(user.find({"email": email}))


def findById(id):
    return list(user.find({"_id": id}))


def updateUserToken(email, token):
    user.update_one({"email": email}, {"$set": {"token": token}})


def updateUserInfo(id, name):
    user.update_one({"_id": id}, {"$set": {"name": name}})
