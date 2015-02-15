__author__ = 'brettlarder'

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('send_queued_mail')

        self.stdout.write('Minutely command executed')
