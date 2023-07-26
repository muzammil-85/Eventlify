from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import RegisterEvent, RegistrationDetail, RegisterorganizerList
from .views import EnrollmentReport, RegistrationReport, TransactionReport
from .razorpay import payment_view, payment_success_view

urlpatterns = [
    path('payment/', payment_view, name='payment'),
    path('payment/success/', payment_success_view, name='payment_success'),
    path('<slug>/register-event', RegisterEvent.as_view(), name='register_event'),
    path('<slug>/organizer-list', login_required(RegisterorganizerList.as_view()), name='register_organizer_list'),
    path('<registration_id>/detail', login_required(RegistrationDetail.as_view()), name='registration_detail'),
    path('<slug>/print-enroll-list', login_required(EnrollmentReport.as_view()), name='print_enroll_list'),
    path('<slug>/print-organizer-list', login_required(RegistrationReport.as_view()), name='print_organizer_list'),
    path('<slug>/print-transaction-list', login_required(TransactionReport.as_view()), name='print_transaction_list'),
]
