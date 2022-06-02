from app.domain.User import User


def save(user):
    return user.save()


def findByEmail(email):
    return User.objects(email=email)


def find_by_id(id):
    return User.objects(id=id)
