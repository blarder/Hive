__author__ = 'brettlarder'

from rest_framework import serializers

from channels.models import Channel
from events.models import Event
from ..models import AdminWarning, UserMessage

from events.serializers import EventSerializerForManagement, EventSerializer
from channels.serializers import ChannelSerializer
from .users import UserSerializer, UserSerializerForManagement

class AdminWarningSerializer(serializers.ModelSerializer):
    staff_member = UserSerializerForManagement()
    being_processed_by = UserSerializer()
    event = EventSerializerForManagement()

    class Meta:
        model = AdminWarning
        fields = ('id', 'staff_member', 'event', 'time', 'detail', 'being_processed_by')


class UserMessageSerializer(serializers.ModelSerializer):

    event = EventSerializer(required=False)

    class Meta:
        model = UserMessage
        fields = ('id', 'event', 'headline', 'detail', 'time')


class UserMessageSerializerForManagement(UserMessageSerializer):

    channels = ChannelSerializer(many=True, required=False)

    class Meta:
        model = UserMessage
        fields = ('id', 'event', 'channels', 'headline', 'detail', 'time')


class UserMessageSerializerForCreation(UserSerializerForManagement):

    channels = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all(), many=True, required=False)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
