__author__ = 'brettlarder'

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        #TODO: Send email warning to bank staff who have gone too long without taking a shift
        #TODO: Notify Employment Plus when a bank staff member has been on the bank for a certain duration
        self.stdout.write('Daily command executed')
