__author__ = 'brettlarder'
from celery import shared_task
from .models import APNSDevice, GCMDevice
from users.models import Shift

@shared_task
def send_notifications():
    #TODO: decide how to filter
    APNSDevice.objects.filter(user__username='brett').send_message('testing')
    GCMDevice.objects.filter(user__username='brett').send_message('testing')
