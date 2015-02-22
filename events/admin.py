from django.contrib import admin
from .models import EventLog, Event


class EventLogInline(admin.TabularInline):
    model = EventLog
    can_delete = False
    def get_readonly_fields(self, request, obj=None):
        return "text", "time"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EventAdmin(admin.ModelAdmin):

    fields = ['channels', 'start', 'end', 'location', 'detail']
    inlines = [EventLogInline]

admin.site.register(Event, EventAdmin)
