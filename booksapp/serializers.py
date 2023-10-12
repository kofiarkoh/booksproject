from rest_framework import serializers
from booksapp.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'password', 'first_name', 'last_name', 'username', 'email']
        extra_kwargs = {'password': {'write_only': True}}

