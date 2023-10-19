from django.urls import path, include
from analytics import views
from django.conf.urls.static import static
from django.conf import settings
from menu import views

urlpatterns = [
    path('about/', views.about, name='_about'),
    path('',include('accounts.urls')), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)