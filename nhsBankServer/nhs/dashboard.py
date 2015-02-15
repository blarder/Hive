"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'nhsBankServer.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from events.models import EventLog

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

class EventLogLinkList(modules.LinkList):

    def get_children(self):
        logs = EventLog.objects.order_by('-time')[:10]
        return [{
            'title': log.text,
            'url': log.event.get_admin_url(),
            'external': False,
            'description': log.text
        } for log in logs]

    def init_with_context(self, context):
        if self._initialized:
            return
        new_children = []
        for link in self.get_children():
            if isinstance(link, (tuple, list,)):
                link_dict = {'title': link[0], 'url': link[1]}
                if len(link) >= 3:
                    link_dict['external'] = link[2]
                if len(link) >= 4:
                    link_dict['description'] = link[3]
                new_children.append(link_dict)
            else:
                new_children.append(link)
        self.children = new_children
        self._initialized = True


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    title = 'Hive Editor'
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Group: Administration & Applications'),
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    _('Administration'),
                    column=1,
                    models=(
                        'django.contrib.*',
                        'rest_framework.authtoken.models.Token'),
                ),
                modules.AppList(
                    _('Applications'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=(
                        'post_office.models.Email',
                        'users.models.*',
                        'devices.models.*'
                    ),
                )
            ]
        ))
        """
        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('AppList: Applications'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            exclude=('django.contrib.*',),
        ))
        
        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('ModelList: Administration'),
            column=1,
            collapsible=False,
            models=('django.contrib.*',),
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Google-Code'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
            ]
        ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Shift Updates'),
            column=2,
            feed_url='/users/latestfeed/',
            limit=5
        ))
        """
        self.children.append(EventLogLinkList(title='Recent Updates', column=2))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=10,
            collapsible=False,
            column=3,
        ))


