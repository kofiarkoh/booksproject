import logging
from random import randrange
from datetime import datetime
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
from django.utils import timezone
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from mail_templated import EmailMessage
from booksapp.serializers import UserSerializer, BookSerializer, RequestPasswordResetTokenSerializer, VerifyPasswordResetTokenSerializer
from booksapp.models import Book, User, OTP
from booksapp.tasks import send_password_reset_otp

from knox.models import AuthToken
# import logg
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
        _ , token = AuthToken.objects.create(user)

        return Response({
            'user'  : UserSerializer(user).data,
            'token' : token
        })

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
                otp = OTP(user=user, code=f"{randrange(0000,9999)}")
                otp.save()

                #message = EmailMessage('mail/password_reset_otp.html',
                #                       {},from_email='t@gmail.com',to=['u@gmail.com']
                #                       )
                #message.content_subtype
                #message.send()
                send_password_reset_otp.delay()
                return Response("send the token")

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({
                'message' : 'No account exists with the provided email'
            }, status=status.HTTP_404_NOT_FOUND)


class VerifyPasswordResetOTPView(APIView):

    def post(self, request, format=None):
        try:
            data = JSONParser().parse(request)
            serializer = VerifyPasswordResetTokenSerializer(data=data)

            if serializer.is_valid():
                otp = OTP.objects.get(code=serializer.validated_data['token'])
                current_time = timezone.now()
                diff_in_minutes = (current_time - otp.created_at)
                diff_in_minutes = diff_in_minutes.total_seconds() / 60
                if diff_in_minutes> 5:
                    return Response({
                        'message': 'OTP token expired',
                    }, status=status.HTTP_400_BAD_REQUEST)

                otp.delete()
                return Response(
                    {
                        'message': 'OTP verified successfully',
                    }
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({
                'message' : 'Invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)
