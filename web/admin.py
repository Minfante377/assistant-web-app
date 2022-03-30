from web.forms import ClientForm, OwnerForm
from web.models import Calendar, Client, Event, Owner

from django.contrib import admin


class CalendarAdmin(admin.ModelAdmin):
    """
    This class defines the Calendar Admin page.
    """
    list_display = ['summary', 'owner']


class ClientAdmin(admin.ModelAdmin):
    """
    This class defines the Client Admin page.
    """
    add_form = ClientForm
    form = ClientForm
    list_display = ['first_name', 'last_name', 'email', 'identity_number']
    model = Client

    add_fieldsets = (None, {
            'classes': ('wide'),
            'fields': ('first_name', 'last_name', 'email', 'identity_number',
                       'password')})


class EventAdmin(admin.ModelAdmin):
    """
    This class defines the Event Admin page.
    """
    list_display = ['day', 'start_time', 'end_time', 'location', 'client',
                    'free', 'calendar']


class OwnerAdmin(admin.ModelAdmin):
    """
    This class defines the Owner Admin page.
    """
    add_form = OwnerForm
    form = OwnerForm
    list_display = ['email', 'owner_id']
    model = Owner

    add_fieldsets = (None, {
            'classes': ('wide'),
            'fields': ('email', 'password')})


admin.site.register(Calendar, admin_class=CalendarAdmin)
admin.site.register(Client, admin_class=ClientAdmin)
admin.site.register(Event, admin_class=EventAdmin)
admin.site.register(Owner, admin_class=OwnerAdmin)
