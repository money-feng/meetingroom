from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('perms/', views.PermissionPIView.as_view()),
    path('users/', views.UserInfosAPIView.as_view()),
    path('users/<str:query>', views.UserInfosAPIView.as_view()),
    path('roles/', views.RolsAPIView.as_view()),
    path('roles/<str:query>', views.RolsAPIView.as_view()),


]