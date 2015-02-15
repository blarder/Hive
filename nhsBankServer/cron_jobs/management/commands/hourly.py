__author__ = 'brettlarder'

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('send_notifications')
        self.stdout.write('Hourly command executed')
