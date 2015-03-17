from functools import reduce

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType

from post_office import mail

from channels.models import Channel
from events.models import Event


class UserManager(BaseUserManager):

    def get_by_natural_key(self, username):
        return super().get_by_natural_key(username.lower())

    def _create_user(self, username, email, password, is_staff, is_superuser,
                     **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):

        return self._create_user(username, email, password, True, True,
                                 **extra_fields)

    def users_for_channels(self, channels):
        query_sets = [channel.subscribers.all() for channel in channels]
        return reduce(lambda x, y: x | y, query_sets) if query_sets else []

    def users_for_event(self, event):
        return self.users_for_channels(event.channels)


class User(AbstractUser):
    verified = models.BooleanField(default=False)
    subscriptions = models.ManyToManyField(Channel, related_name='subscribers')
    forgotten_password_key = models.CharField(max_length=255)
    objects = UserManager()

    def __str__(self):
        return self.username

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model),
                                    args=(self.id,))

    def reset_password(self):
        """

        """

        self.forgotten_password_key = get_random_string()

        self.save()

        mail.send(
            self.email,
            settings.EMAIL_HOST_USER,
            subject='Password reset',
            message='Your forgotten password key is: \n{}\n '
                    'You can use this key to set a new password.'.format(self.forgotten_password_key)
        )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if type(self.username) is str:
            self.username = self.username.lower()
            self.first_name = self.first_name.title()
            self.last_name = self.last_name.title()

        if not self.pk:
            just_created = True
        else:
            just_created = False

        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)

        if just_created:
            warning = AdminWarning(staff_member=self, detail='New account requires verification')
            warning.save()


class AdminWarning(models.Model):
    staff_member = models.ForeignKey(User, null=True, blank=True, default=None)
    event = models.ForeignKey(Event, null=True, blank=True, default=None)
    detail = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    being_processed_by = models.ForeignKey(User, null=True, blank=True, default=None,
                                           related_name='warnings_processing')


class UserMessageManager(models.Manager):
    def messages_for_channels(self, channels):
        query_sets = [channel.messages.all() for channel in channels]
        return reduce(lambda x, y: x | y, query_sets) if query_sets else []

    def messages_for_user(self, user):
        return self.messages_for_channels(user.subscriptions.all()) if user.verified else []


class UserMessage(models.Model):
    event = models.ForeignKey(Event, null=True, blank=True, default=None)
    channels = models.ManyToManyField(Channel, blank=True, default=[], related_name='messages')
    headline = models.CharField(max_length=255)
    detail = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    objects = UserMessageManager()
    #TODO: store messages for each notification sent in the last 24hr

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.event and self.pk is not None:
            self.channels = self.event.channels.all()

        super().save(force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)


class UserAttribute(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, blank=True, default=[], related_name='attributes')
