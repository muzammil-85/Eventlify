from django.contrib import admin

from .models import EventRecord, Client,Answer

admin.site.register(EventRecord)
admin.site.register(Client)
admin.site.register(Answer)
