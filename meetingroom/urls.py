from django.urls import path
from . import views


urlpatterns = [
    path('', views.MeetingRoomApiView.as_view()),
    path('<int:id>', views.MeetingRoomApiView.as_view())
]