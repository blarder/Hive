__author__ = 'brettlarder'
from django.db.models.signals import post_save, post_delete, m2m_changed
from rest_framework.renderers import JSONRenderer

from events.models import Event, EventLog, Location
from channels.models import Channel
from .models import AdminWarning, User, UserMessage

from events.serializers import EventSerializerForManagement, EventLogSerializer, LocationSerializer
from channels.serializers import ChannelSerializer
from .serializers.messages import AdminWarningSerializer, UserMessageSerializerForManagement
from .serializers.users import UserSerializerForManagement

import redis


def push_data_to_redis(serializer_class, channel_name, message_type, **kwargs):

    def wrapped(sender, instance, **_):
        data = serializer_class(instance).data
        data['message_type'] = message_type
        data.update(kwargs)
        json = JSONRenderer().render(data)
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish(channel_name, json)

        print('pushed message: {}'.format(json))

    return wrapped


def push_m2m_user_data_to_redis(sender, instance, action, reverse, *args, **kwargs):
    if action == 'post_add' and not reverse:
        data = UserSerializerForManagement(instance).data
        data['message_type'] = 'user'
        json = JSONRenderer().render(data)
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('admin', json)


def push_m2m_event_data_to_redis(sender, instance, action, reverse, *args, **kwargs):
    if action == 'post_add' and not reverse:
        data = EventSerializerForManagement(instance).data
        data['message_type'] = 'event'
        json = JSONRenderer().render(data)
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('admin', json)


#TODO: use django.db.models.signals.m2m_changed --
#see http://stackoverflow.com/questions/15898829/manytomanyfield-is-empty-in-post-save-function

post_save.connect(push_data_to_redis(EventSerializerForManagement, 'admin', 'event'), sender=Event, weak=False)
post_save.connect(push_data_to_redis(EventLogSerializer, 'admin', 'event_log'), sender=EventLog, weak=False)
post_save.connect(push_data_to_redis(AdminWarningSerializer, 'admin', 'warning'), sender=AdminWarning, weak=False)
post_save.connect(push_data_to_redis(UserSerializerForManagement, 'admin', 'user'), sender=User, weak=False)
post_save.connect(push_data_to_redis(ChannelSerializer, 'admin', 'channel'), sender=Channel, weak=False)
post_save.connect(push_data_to_redis(UserMessageSerializerForManagement, 'admin', 'user_message'), sender=UserMessage,
                  weak=False)
post_save.connect(push_data_to_redis(LocationSerializer, 'admin', 'location'), sender=Location, weak=False)

m2m_changed.connect(push_m2m_user_data_to_redis, sender=User.subscriptions.through, weak=False)
m2m_changed.connect(push_m2m_event_data_to_redis, sender=Event.channels.through, weak=False)

post_delete.connect(push_data_to_redis(EventSerializerForManagement, 'admin', 'event_deletion'), sender=Event,
                    weak=False)
post_delete.connect(push_data_to_redis(AdminWarningSerializer, 'admin', 'warning_deletion'), sender=AdminWarning,
                    weak=False)
post_delete.connect(push_data_to_redis(UserMessageSerializerForManagement, 'admin', 'user_message_deletion'),
                    sender=UserMessage, weak=False)
