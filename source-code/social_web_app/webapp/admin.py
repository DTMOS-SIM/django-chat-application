from django.contrib import admin
from .models import *

admin.site.register(AppUser)
admin.site.register(Images)
admin.site.register(Chats)
admin.site.register(Rooms)
