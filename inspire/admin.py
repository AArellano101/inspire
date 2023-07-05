from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(InspireUser, UserAdmin)
admin.site.register(UserMessage)
admin.site.register(Text)
admin.site.register(Notification)