__author__ = 'brettlarder'
from rest_framework import generics

from . import serializers, models


class ChannelList(generics.ListCreateAPIView):

    serializer_class = serializers.ChannelSerializer
    queryset = models.Channel.objects.all()


class ChannelDetail(generics.RetrieveAPIView):

    serializer_class = serializers.ChannelSerializer
    queryset = models.Channel.objects.all()
