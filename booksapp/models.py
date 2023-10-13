from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager


# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']


class Book(models.Model):
    user = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    description = models.CharField(max_length=200)

class OTP(models.Model):
    user = models.ForeignKey(User,related_name='otps',on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)



