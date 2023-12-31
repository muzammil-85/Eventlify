from rest_framework import viewsets
from . import models
from . import serializer as serializers

class EventRecordViewset(viewsets.ModelViewSet):
    queryset =  models.EventRecord.objects.all()
    serializer_class = serializers.EventRecordSerializer


# this view set automatically make some functions which are:
# create()
# retrieve() => only retrieve one data
# list() => same as retrieve but retrieve multiple data
# update()
# destroy()