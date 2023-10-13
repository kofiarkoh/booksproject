from rest_framework import serializers
from booksapp.models import User
from booksapp.models import Book


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'first_name', 'last_name', 'username', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class BookSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'user']


class RequestPasswordResetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
