from django.urls import path, include
from administration import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('publish_object', views.publish_object, name='publish_object'),
    path('publish_object_', views.publish_object_, name ='publish_object_'),
    path('my_objects', views.my_objects, name='my_objects'), 
    path('edit_object/<int:object_id>/', views.edit_object, name='edit_object'),
    path('delete_object/<int:object_id>/', views.delete_object, name='delete_object'),
    path('',include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)