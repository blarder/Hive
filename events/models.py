import datetime
from functools import reduce

from django.db import models
from django.conf import settings
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType

from channels.models import Channel


class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class EventTag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class EventManager(models.Manager):

    def events_for_channels(self, channels):
        query_sets = [channel.events.all() for channel in channels]
        return reduce(lambda x, y: x | y, query_sets).filter(end__gt=datetime.datetime.now()) if query_sets else []

    def events_for_user(self, user):
        """
        These are the events the user will be able to see
        """
        if user.is_staff:
            # .filter(end__gt=datetime.datetime.now())\ may be needed
            return self.get_queryset()\
                .select_related('tags', 'location', 'being_processed_by', 'channels')

        if not user.is_authenticated() or not user.verified:
            return []

        return self.events_for_channels(user.subscriptions.all())


class Event(models.Model):
    tags = models.ManyToManyField(EventTag, related_name='events', blank=True, default=[])
    channels = models.ManyToManyField(Channel, related_name='events', blank=True, default=[])
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.ForeignKey(Location, related_name='events')
    detail = models.CharField(max_length=255, null=True, blank=True, default=None)
    being_processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None,
                                           related_name='events_processing')
    public = models.BooleanField(default=True)
    spaces = models.IntegerField(default=1)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='events_attending',
                                       blank=True, default=[])

    objects = EventManager()

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model),
                                    args=(self.id,))

    def __str__(self):
        return self.detail


class EventLog(models.Model):
    event = models.ForeignKey(Event, related_name='log')
    text = models.TextField(blank=True, default='')
    time = models.DateTimeField(auto_now_add=True)
