from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('menu/', views.MenuListAPIView.as_view()),
    path('users/', views.UserInfosAPIView.as_view()),
    path('users/<str:name>', views.UserInfosAPIView.as_view()),
    path('users/<int:id>', views.UserInfosAPIView.as_view())

]