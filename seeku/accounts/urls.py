from django.urls import path, include
from accounts import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)