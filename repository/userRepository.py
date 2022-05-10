from config.db import user
from domain.User import User


def save(form: User):
    user.insert_one({"name": User.get__name(), "email": User.get__email(), "passwd": User.get__passwd()})
