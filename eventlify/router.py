
from event.viewset import EventRecordViewset,DataListViewset
from registration.viewset import TransactionRecordViewset,RegistrationRecordViewset
from organizer.viewset import organizerRecordViewset
from  rest_framework import routers

router = routers.DefaultRouter()
router.register('event',EventRecordViewset)
router.register('data_list',DataListViewset)
router.register('transaction_record',TransactionRecordViewset)
router.register('registration_record',RegistrationRecordViewset)
router.register('organizer_record',organizerRecordViewset)
 
# url will be like this :
#   localhost:8000/api/employee/
# methods are GET , POST , PUT , DELETE