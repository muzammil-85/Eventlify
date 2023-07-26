from django.contrib import admin

from .models import EventRecord, DataList, Client,Answer

admin.site.register(EventRecord)
admin.site.register(DataList)
admin.site.register(Client)
admin.site.register(Answer)
