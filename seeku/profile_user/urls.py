from django.urls import path, include
from analytics import views
from django.conf.urls.static import static
from django.conf import settings
from profile_user import views

urlpatterns = [
    path('edit_profile_view/', views.edit_profile_view, name='edit_profile_view'),
    path('edit_profile_view_es/', views.edit_profile_view_es, name='edit_profile_view_es'),
    path('my_profile', views.my_profile, name='my_profile'),   
    path('my_profile_es', views.my_profile_es, name='my_profile_es'),  
    path('',include('accounts.urls')), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)