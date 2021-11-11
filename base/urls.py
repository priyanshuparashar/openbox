from django.urls import path
from . import views

urlpatterns = [
    path('loginr/', views.loginr, name="loginr"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="registerUser"),
    
    path('test/', views.tests, name="tests"),
    path('',views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('userprofile/<str:pk>/', views.userprofile, name="userprofile"),
    path('web/', views.web),
    path('createroom/', views.createroom, name="createroom"),
    path('updateroom/<str:pk>/', views.updateroom, name="updateroom"),
    path('deleteroom/<str:pk>/', views.deleteroom, name="deleteroom"),
    path('contact/', views.contact, name="contact")


]
