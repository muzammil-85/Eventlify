from rest_framework import viewsets
from . import models
from . import serializer as serializers

class TransactionRecordViewset(viewsets.ModelViewSet):
    queryset =  models.TransactionRecord.objects.all()
    serializer_class = serializers.TransactionRecordSerializer

class RegistrationRecordViewset(viewsets.ModelViewSet):
    queryset =  models.RegistrationRecord.objects.all()
    serializer_class = serializers.RegistrationRecordSerializer

# this view set automatically make some functions which are:
# create()
# retrieve() => only retrieve one data
# list() => same as retrieve but retrieve multiple data
# update()
# destroy()