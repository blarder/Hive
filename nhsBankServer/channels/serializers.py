__author__ = 'brettlarder'

from rest_framework import serializers

from .models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
