from django.contrib import admin

# Register your models here.
from .models import User, Roster, Checkinbook, Checkinsheet, Checkinitem, Location, UserIdentitycodeCheckinsheetBond

admin.site.register(User)
admin.site.register(Roster)
admin.site.register(Checkinbook)
admin.site.register(Checkinsheet)
admin.site.register(Checkinitem)
admin.site.register(Location)
admin.site.register(UserIdentitycodeCheckinsheetBond)