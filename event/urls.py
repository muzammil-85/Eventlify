from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import AddEvent, EventDetail, UpdateEvent, DeleteEvent, EventListView, showform, createform, updateform

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('add-event', login_required(AddEvent.as_view()), name='add_event'),
    path('<slug>/event-form/', login_required(showform), name='event_form'),
    path('<slug>/create-form/',login_required(createform), name='create_form'),
    path('<slug>/update-form/',login_required(updateform), name='update_form'),
    path('<slug>/event-detail', EventDetail.as_view(), name='event_detail'),
    path('<slug>/update-event', login_required(UpdateEvent.as_view()), name='update_event'),
    path('<slug>/delete/<timestamp>', login_required(DeleteEvent.as_view()), name='delete_event'),
]