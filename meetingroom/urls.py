from django.urls import path
from . import views


urlpatterns = [
    path('', views.MeetingRoomApiView.as_view())
]