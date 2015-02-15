__author__ = 'brettlarder'
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from devices.models import SMSDevice, GCMDevice, APNSDevice
from devices.serializers import GCMDeviceSerializer, APNSDeviceSerializer, SMSDeviceSerializer

from users.models import UserMessage
from events.models import Event

from users.serializers.users import UserSerializerWithFullSubscriptions
from users.serializers.messages import UserMessageSerializer
from events.serializers import EventSerializer


class AllUserData(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        user_serializer = UserSerializerWithFullSubscriptions(request.user)
        events_serializer = EventSerializer(Event.objects.events_for_user(self.request.user), many=True)
        user_messages_serializer = UserMessageSerializer(UserMessage.objects.messages_for_user(self.request.user),
                                                         many=True)

        apns_device_serializer = APNSDeviceSerializer(APNSDevice.objects.filter(user=request.user), many=True)
        gcm_device_serializer = GCMDeviceSerializer(GCMDevice.objects.filter(user=request.user), many=True)
        sms_device_serializer = SMSDeviceSerializer(SMSDevice.objects.filter(user=request.user), many=True)

        return Response({
            'user': user_serializer.data,
            'events': events_serializer.data,
            'devices': apns_device_serializer.data + gcm_device_serializer.data + sms_device_serializer.data,
            'messages': user_messages_serializer.data
        }, status=status.HTTP_200_OK)
