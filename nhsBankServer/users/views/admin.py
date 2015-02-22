__author__ = 'brettlarder'
from rest_framework.views import APIView, Response, status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.renderers import JSONRenderer
import redis

from ..serializers.messages import AdminWarningSerializer, UserMessageSerializerForManagement,\
    UserMessageSerializerForCreation
from ..tasks import send_push_notifications_for_event, create_user_message
from ..models import AdminWarning, UserMessage


class AdminMessageView(APIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('admin', JSONRenderer().render({
            'message_type': 'chat',
            'sender': request.user.username,
            'comment': request.DATA['comment']
        }))

        return Response(status=status.HTTP_200_OK)


class UserMessageView(APIView):

    # Create user message here, and only send push notifications if a relevant flag is set to true

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        try:
            if request.DATA.get('push'):
                send_push_notifications_for_event.delay(request.DATA.get('event_id'), request.DATA.get('note'))
            return Response(status=status.HTTP_200_OK)

        except (TypeError, KeyError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserMessageList(generics.ListCreateAPIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminUser, )
    queryset = UserMessage.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserMessageSerializerForCreation
        return UserMessageSerializerForManagement

    def create(self, request, *args, **kwargs):
        create_user_message.delay(request.DATA)
        return Response(status=status.HTTP_201_CREATED)


class UserMessageDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminUser, )
    queryset = UserMessage.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserMessageSerializerForCreation
        return UserMessageSerializerForManagement


class AdminWarningList(generics.ListAPIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminUser, )
    serializer_class = AdminWarningSerializer
    queryset = AdminWarning.objects.all()


class AdminWarningDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminUser, )
    serializer_class = AdminWarningSerializer
    queryset = AdminWarning.objects.all()
