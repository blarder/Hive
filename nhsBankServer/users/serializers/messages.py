__author__ = 'brettlarder'

from rest_framework import serializers

from ..models import AdminWarning, UserMessage
from events.serializers import EventSerializerForManagement, EventSerializer
from .users import UserSerializer, UserSerializerForManagement

class AdminWarningSerializer(serializers.ModelSerializer):
    staff_member = UserSerializerForManagement()
    being_processed_by = UserSerializer()
    event = EventSerializerForManagement()

    class Meta:
        model = AdminWarning
        fields = ('id', 'staff_member', 'event', 'time', 'detail', 'being_processed_by')


class UserMessageSerializer(serializers.ModelSerializer):

    event = EventSerializer()

    class Meta:
        model = UserMessage
        fields = ('id', 'event', 'headline', 'detail', 'time')