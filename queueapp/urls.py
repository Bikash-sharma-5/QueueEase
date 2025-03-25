from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.home, name='home'),
    
    path('accounts/', include('allauth.urls')),
    path('business/<int:business_id>/create_queue/', views.create_queue, name='create_queue'),
    path('business/<int:business_id>/', views.business_detail, name='business_detail'),
    path('register/', views.register, name='register'),
    path('register-business/', views.register_business, name='register_business'),
    path('login/', views.user_login, name='login'),
    path('create-queue/', views.create_queue, name='create_queue'),
    path('logout/', views.logout, name='logout'),
    path('queue/<int:queue_id>/qr/', views.view_qr, name='view_qr'),
    path("queue-success/<int:queue_id>/<int:participant_id>/", views.queue_success, name="queue_success"),
    path('queue/<int:queue_id>/', views.queue_detail, name='queue_detail'),
    path('create-queue/<int:business_id>/', views.create_queue, name='create_queue'),
    path('join-queue/<int:queue_id>/', views.join_queue, name='join_queue'),
    path('complete-participant/<int:participant_id>/', views.complete_participant, name='complete_participant'),
    
]
