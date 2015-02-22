__author__ = 'brettlarder'
from rest_framework import serializers

from .models import Location, Event, EventLog, EventTag
from channels.models import Channel
from channels.serializers import ChannelSerializer
from users.serializers.users import UserSerializer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location


class EventTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTag


class EventSerializer(serializers.ModelSerializer):

    location = LocationSerializer()
    tags = EventTagSerializer(many=True, required=False)
    channels = ChannelSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'start', 'end', 'location', 'tags', 'channels')


class EventLogSerializer(serializers.ModelSerializer):

    event_id = serializers.IntegerField(source='event.id')

    class Meta:
        model = EventLog
        fields = ('id', 'text', 'time', 'event_id')


class EventSerializerForManagement(EventSerializer):

    being_processed_by = UserSerializer(required=False)
    log = EventLogSerializer(many=True, required=False)
    admin_url = serializers.CharField(source='get_admin_url', read_only=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'start', 'end', 'location',
                  'detail', 'being_processed_by',
                  'log', 'public', 'tags', 'channels', 'admin_url')
        read_only_fields = ('admin_url', )


class EventSerializerForCreation(EventSerializerForManagement):

    channels = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all(), many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=EventTag.objects.all(), many=True)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
