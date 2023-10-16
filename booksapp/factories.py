from factory import Factory, Faker
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory
from booksapp.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    username = Faker('name')
    email = Faker('email')
    password = make_password('password')
