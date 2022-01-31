from django.contrib import admin

from . import models

admin.site.register(models.Venue)
admin.site.register(models.myClubUser)
admin.site.register(models.Event)

