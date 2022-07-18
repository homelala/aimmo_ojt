from app.domain.user import User


def save(user):
    return user.save()


def findByEmail(email):
    return User.objects(email=email)


def find_by_id(id):
    return User.objects(id=id)


def find_by_id(id):
    return User.objects(id=id)
