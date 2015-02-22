__author__ = 'brettlarder'
from django.core.management.base import BaseCommand
from ...tasks import send_notifications


class Command(BaseCommand):
    can_import_settings = True
    help = 'Send out notifications aynchronously'

    def handle(self, *args, **options):
        job = send_notifications.delay()
        self.stdout.write('Notification job sent (id: {})'.format(job.id))
