from django.urls import path
from . import views


urlpatterns = [
    path('meeting/', views.MeetingRoomApiView.as_view()),
    path('meeting/<int:id>', views.MeetingRoomApiView.as_view()),
    path('reserve/', views.MeetingRecordsApiView.as_view()),
    path('reserve/<int:id>', views.MeetingRecordsApiView.as_view()),
    path('equipment/', views.EquipmentAPIView.as_view())
]