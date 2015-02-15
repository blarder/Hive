__author__ = 'brettlarder'

from celery import shared_task
from devices.models import APNSDevice, GCMDevice

from events.models import Event, EventLog
from .models import AdminWarning, UserMessage, User


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
