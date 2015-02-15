from django.db import transaction

from rest_framework import generics, permissions, response, status, authentication

from . import models
from . import serializers


class EventList(generics.ListCreateAPIView):

    permission_classes = (permissions.IsAuthenticated, )

    serializer_class = serializers.EventSerializer

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return serializers.EventSerializerForCreation if self.request.method == 'POST' \
                else serializers.EventSerializerForManagement
        return serializers.EventSerializer

    def get_queryset(self):
        return models.Event.objects.events_for_user(self.request.user)

    def create(self, request, *args, **kwargs):

        if not request.user.is_staff:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

        return super().create(request, *args, **kwargs)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    allowed_methods = ['GET', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return serializers.EventSerializerForManagement

        return serializers.EventSerializer

    def create_log_object(self, log_message):
        log = models.EventLog(event=self.get_object(), text=log_message)
        log.save()

    def update_processor(self, processor):
        event_object = self.get_object()
        event_object.being_processed_by = processor
        event_object.save()

        return response.Response(status=status.HTTP_200_OK)

    def patch_with_log(self, data, log_message):
        serializer = self.get_serializer_class()(self.get_object(), data, partial=True)

        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                self.create_log_object(log_message)

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        # Consider transaction here to ensure double booking is not possible

        if request.user.is_staff:
            # Staff-only commands
            if 'log' in request.DATA:
                try:
                    self.create_log_object(request.DATA['log'])
                    return response.Response(status=status.HTTP_200_OK)

                except (KeyError, IndexError):
                    return response.Response(status=status.HTTP_400_BAD_REQUEST)

            elif request.DATA == 'PROCESS':
                return self.update_processor(self.request.user)

            elif request.DATA == 'DONE':
                return self.update_processor(None)

            else:
                return super().update(request, *args, **kwargs)

        return response.Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

class LocationList(generics.ListCreateAPIView):

    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()


class LocationDetail(generics.RetrieveAPIView):

    serializer_class = serializers.ChannelSerializer
    queryset = models.Location.objects.all()

class EventTagList(generics.ListCreateAPIView):

    serializer_class = serializers.EventTagSerializer
    queryset = models.EventTag.objects.all()


class EventTagDetail(generics.RetrieveAPIView):

    serializer_class = serializers.EventTagSerializer
    queryset = models.EventTag.objects.all()

