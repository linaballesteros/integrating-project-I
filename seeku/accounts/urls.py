from django.urls import path, include
from accounts import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_es/', views.login_es, name='login_es'),
    path('register/', views.register, name='register'),
    path('register_es/', views.register_es, name='register_es'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)