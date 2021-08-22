from django.contrib import admin

from .models import Venue
from .models import MyClubUser
from .models import Event
# Register your models here.

#admin.site.register(Venue)
admin.site.register(MyClubUser)
#admin.site.register(Event)


#Change order om
#Modify Venue Admin Area (not need migrations)
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name","address","phone")
    ordering = ("name",)  #Change order on Django admin Page by name
    search_fields = ("name","address") #Add search Function to Admin area


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (("name","venue"), "event_date","description" ,"manager")
    list_display = ("name","event_date","venue")
    list_filter = ("event_date","venue")
    ordering = ("-event_date",)  #need a , beacuse it's a tuple - order by negative order -
