from django.urls import path, include
from analytics import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('analytics/', views.analytics, name='_analytics'),
    path('analytics_es/', views.analytics_es, name='_analytics_es'),
    #path('',include('accounts.urls')),
    path('Path.html', views.map_view, name='map_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)