from rest_framework import viewsets
from . import models
from . import serializer as serializers

class organizerRecordViewset(viewsets.ModelViewSet):
    queryset =  models.organizerRecord.objects.all()
    serializer_class = serializers.organizerRecordSerializer



# this view set automatically make some functions which are:
# create()
# retrieve() => only retrieve one data
# list() => same as retrieve but retrieve multiple data
# update()
# destroy()