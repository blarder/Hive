from django.contrib import admin

from . import signals
from .models import User

class UserAdmin(admin.ModelAdmin):

    fields = ['username', 'first_name', 'last_name', 'email', 'subscriptions', 'verified']

admin.site.register(User, UserAdmin)
