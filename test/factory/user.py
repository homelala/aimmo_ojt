import factory
from factory.mongoengine import MongoEngineFactory

from app.domain.User import User


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    name = factory.Faker("name")
    passwd = factory.Faker("password", length=30, special_chars=True, digits=True, upper_case=True, lower_case=True)
