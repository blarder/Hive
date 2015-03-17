__author__ = 'brettlarder'
from rest_framework import serializers

from channels.models import Channel
from ..models import User

from devices.serializers import APNSDeviceSerializer, GCMDeviceSerializer, SMSDeviceSerializer
from channels.serializers import ChannelSerializer


class UserSerializer(serializers.ModelSerializer):
    smsdevice_set = SMSDeviceSerializer(many=True, read_only=True)
    apnsdevice_set = APNSDeviceSerializer(many=True, read_only=True)
    gcmdevice_set = GCMDeviceSerializer(many=True, read_only=True)

    subscriptions = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all(), many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'subscriptions',
                  'smsdevice_set', 'apnsdevice_set','gcmdevice_set',
                  'verified', 'first_name', 'last_name')

        write_only_fields = ('password',)
        read_only_fields = ('verified',)


class UserSerializerWithFullSubscriptions(UserSerializer):
    subscriptions = ChannelSerializer(many=True, read_only=True)

class UserSerializerForManagement(UserSerializerWithFullSubscriptions):
    admin_url = serializers.CharField(source='get_admin_url')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'subscriptions',
                  'smsdevice_set', 'apnsdevice_set','gcmdevice_set',
                  'verified', 'first_name', 'last_name', 'admin_url')

        write_only_fields = ('password',)
