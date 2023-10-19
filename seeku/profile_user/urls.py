from django.urls import path, include
from analytics import views
from django.conf.urls.static import static
from django.conf import settings
from profile_user import views

urlpatterns = [
    path('edit_profile_view/', views.edit_profile_view, name='edit_profile_view'),
    path('my_profile', views.my_profile, name='my_profile'),    
    path('',include('accounts.urls')), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)