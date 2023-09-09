from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import RegisterEvent, RegisterParticipantList, RegistrationDetail
from .views import EnrollmentReport, RegistrationReport, TransactionReport
from .views import payment_view, payment_success_view,ticket

urlpatterns = [
    path('<slug>/payment/', payment_view, name='payment'),
    path('<slug>/payment/success', payment_success_view, name='payment_success'),
    path('<slug>/ticket/', ticket, name='ticket'), #timestamp/
    path('<slug>/register-event', RegisterEvent.as_view(), name='register_event'),
    path('<slug>/participant-list', login_required(RegisterParticipantList.as_view()), name='participant_list'),
    path('<registration_id>/detail', login_required(RegistrationDetail.as_view()), name='registration_detail'),
    path('<slug>/print-enroll-list', login_required(EnrollmentReport.as_view()), name='print_enroll_list'),
    path('<slug>/print-organizer-list', login_required(RegistrationReport.as_view()), name='print_organizer_list'),
    path('<slug>/print-transaction-list', login_required(TransactionReport.as_view()), name='print_transaction_list'),
]
