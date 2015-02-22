__author__ = 'brettlarder'
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView, Response, status
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..serializers.users import UserSerializer, UserSerializerWithFullSubscriptions, UserSerializerForManagement
from ..models import User


class MyUserPage(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, format=None):

        serializer = UserSerializerWithFullSubscriptions(request.user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        if 'username' in request.DATA and type(request.DATA['username']) is str:
            request.DATA['username'] = request.DATA['username'].lower()

        if 'password' in request.DATA:
            request.DATA['password'] = make_password(request.DATA['password'])

        serializer = UserSerializer(request.user, request.DATA, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListCreateAPIView):

    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializerWithFullSubscriptions
        return UserSerializer

    def create(self, request, *args, **kwargs):
        if 'username' in request.DATA and type(request.DATA['username']) is str:
            request.DATA['username'] = request.DATA['username'].lower()
        if 'password' in request.DATA:
            request.DATA['password'] = make_password(request.DATA['password'])

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return []


class UserDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAdminUser, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'PATCH':
            return UserSerializerForManagement
        return UserSerializer
