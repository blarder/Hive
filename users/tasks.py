__author__ = 'brettlarder'

from celery import shared_task
from devices.models import APNSDevice, GCMDevice

from channels.models import Channel
from events.models import Event, EventLog
from .models import AdminWarning, UserMessage, User


@shared_task
def create_user_message(message_data):
    event = Event.objects.get(id=message_data['event_id']) if 'event_id' in message_data else None
    if event:
        channels = event.channels.all()
    else:
        channels = Channel.objects.filter(id__in=message_data.get('channels')) if 'channels' in message_data \
            else Channel.objects.all()
    headline = message_data.get('headline')
    detail = message_data.get('detail')

    user_message = UserMessage(headline=headline, detail=detail, event=event)
    user_message.save()

    user_message.channels = channels
    user_message.save()

    if message_data.get('push'):

        eligible_users = User.objects.users_for_channels(channels)

        apns_devices = APNSDevice.objects.filter(user__in=eligible_users)
        gcm_devices = GCMDevice.objects.filter(user__in=eligible_users)

        if apns_devices:
            apns_devices.send_message(headline, sound='default')

        if gcm_devices:
            gcm_devices.send_message(headline)


        log = EventLog(event=event)
        log.text = 'Notifications sent out'
        log.save()


@shared_task
def send_push_notifications_for_event(event_id, message=None):

    if event_id is None:
        return send_mass_notification(message=message)

    event = Event.objects.get(id=event_id)
    if not message:
        message = "EVENT ALERT - PLEASE CHECK APP"
    eligible_users = User.objects.users_for_event(event)
    apns_devices = APNSDevice.objects.filter(user__in=eligible_users)
    gcm_devices = GCMDevice.objects.filter(user__in=eligible_users)

    if apns_devices:
        apns_devices.send_message(message, sound='default')

    if gcm_devices:
        gcm_devices.send_message(message)


    log = EventLog(event=event)
    log.text = 'Notifications sent out'
    log.save()

    user_message = UserMessage(headline='Event Notification', detail=message, event=event)
    user_message.save()


def send_mass_notification(message=None):

    if not message:
        message = "EVENT ALERT - EMERGENCY COVER REQUIRED"

    apns_devices = APNSDevice.objects.all()
    gcm_devices = GCMDevice.objects.all()

    if apns_devices:
        apns_devices.send_message(message, sound='default')

    if gcm_devices:
        gcm_devices.send_message(message)

    warning = AdminWarning(detail='Mass notification sent out')
    warning.save()

    user_message = UserMessage(headline='Notification for all staff', detail=message)
    user_message.save()
