__author__ = 'brettlarder'
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView, Response, status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from social.apps.django_app.utils import psa
from social.backends import oauth

from ..models import User


class LogInPage(APIView):

    def post(self, request, format=None):

        username = request.DATA['username'].lower() if 'username' in request.DATA else ''
        password = request.DATA['password'] if 'password' in request.DATA else ''
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                login(request, user)
            except:
                pass
            return Response({"token": Token.objects.get_or_create(user=user)[0].key,
                             "staff": user.is_staff}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ValidatePage(APIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    def get(self, request, format=None):
        if request.user.is_staff:
            return Response("ACCEPT")

        return Response("DECLINE")


class PasswordChange(APIView):

    def post(self, request, format=None):
        if 'username' in request.DATA and not 'password' in request.DATA: # User is stating they have forgotten password
            try:
                user = User.objects.get(username=request.DATA['username'])
                user.reset_password()

                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        else:  # User is attempting to use the key emailed to them to set a new password
            try:
                user = User.objects.get(username=request.DATA['username'])
                if user.forgotten_password_key and user.forgotten_password_key == request.DATA['key']:
                    user.forgotten_password_key = None
                    user.set_password(request.DATA['password'])
                    user.save()
                    return Response(status=status.HTTP_200_OK)

            finally:
                return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST', ])
@psa('social:complete')
def social_login(request, backend):
    if isinstance(request.backend, oauth.BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, oauth.BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        return Response('Wrong backend type')
    user_data = request.backend.user_data(token, ajax=True)
    try:
        user = User.objects.get(facebook_id=int(user_data['id']))
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
    except Exception as err:
        return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
    return Response({"token": Token.objects.get_or_create(user=user)[0].key}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST', ])
@psa('social:complete')
def retrieve_social_data(request, backend):
    if isinstance(request.backend, oauth.BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, oauth.BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        return Response('Wrong backend type')
    user_data = request.backend.user_data(token, ajax=True)
    return Response(user_data, status=status.HTTP_200_OK)


class LogOutPage(APIView):

    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)
