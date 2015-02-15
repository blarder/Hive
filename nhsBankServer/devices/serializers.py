__author__ = 'brettlarder'
from rest_framework import serializers
from .models import APNSDevice, GCMDevice, SMSDevice


class APNSDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = APNSDevice
        fields = ('id', 'name', 'device_id', 'registration_id', 'user')


class GCMDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = GCMDevice
        fields = ('id', 'name', 'device_id', 'registration_id', 'user')


class SMSDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = SMSDevice
        fields = ('id', 'name', 'phone_number', 'user')
