from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.contrib.auth.hashers import make_password
from booksapp.serializers import UserSerializer


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
