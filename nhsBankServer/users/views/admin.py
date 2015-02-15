__author__ = 'brettlarder'
from rest_framework.views import APIView, Response, status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.renderers import JSONRenderer
import redis

from ..serializers.messages import AdminWarningSerializer
from ..tasks import send_push_notifications_for_event
from ..models import AdminWarning


class MessageView(APIView):

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


class SendPushNotificationsView(APIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        try:
            send_push_notifications_for_event.delay(request.DATA.get('id'), request.DATA.get('note'))
            return Response(status=status.HTTP_200_OK)

        except (TypeError, KeyError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AdminWarningList(generics.ListAPIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminUser, )
    serializer_class = AdminWarningSerializer

    def get_queryset(self):
        return AdminWarning.objects.all()


class AdminWarningDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminUser, )
    serializer_class = AdminWarningSerializer

    def get_queryset(self):
        return AdminWarning.objects.all()
