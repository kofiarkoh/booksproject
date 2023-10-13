from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.contrib.auth import  login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from booksapp.serializers import UserSerializer, BookSerializer, RequestPasswordResetTokenSerializer
from booksapp.models import Book, User

# Create your views here.

class CreateUser(APIView):

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                password=make_password(serializer.validated_data['password'])
            )
            return Response({"user": serializer.data, 'message': 'user created successfully.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        serializer = AuthTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class BooksView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'message' : 'book data store successfully',
                'data' : serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request, format=None):
        books = Book.objects.filter(user_id=request.user.id)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class RequestPasswordResetOTPView(APIView):

    def post(self, request, format=None):

        try:
            data = JSONParser().parse(request)
            serializer = RequestPasswordResetTokenSerializer(data=data)
            if serializer.is_valid():
                user = User.objects.get(email=serializer.validated_data['email'])
                return Response("send the token")

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({
                'message' : 'No account exists with the provided email'
            }, status=status.HTTP_404_NOT_FOUND)