from django.urls import path, include
from analytics import views

urlpatterns = [
    path('analytics/', views.analytics, name='_analytics'),
    path('',include('accounts.urls')),
]