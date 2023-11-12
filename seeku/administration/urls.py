from django.urls import path, include
from administration import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('publish_object', views.publish_object, name='publish_object'),
    path('publish_object_', views.publish_object_, name ='publish_object_'),
    path('my_objects', views.my_objects, name='my_objects'), 
    path('expired_objects', views.expired_objects, name='expired_objects'), 
    path('edit_object/<int:object_id>/', views.edit_object, name='edit_object'),
    path('delete_object/<int:object_id>/', views.delete_object, name='delete_object'),
    path('count_claim_complaint/<int:object_id>/', views.count_claim_complaint, name='count_claim_complaint'),
    
    path('publish_object_es', views.publish_object_es, name='publish_object_es'),
    path('publish_object__es', views.publish_object__es, name ='publish_object__es'),
    path('my_objects_es', views.my_objects_es, name='my_objects_es'), 
    path('expired_objects_es', views.expired_objects_es, name='expired_objects_es'), 
    path('edit_object_es/<int:object_id>/', views.edit_object_es, name='edit_object_es'),
    path('delete_object_es/<int:object_id>/', views.delete_object_es, name='delete_object_es'),
    path('count_claim_complaint_es/<int:object_id>/', views.count_claim_complaint_es, name='count_claim_complaint_es'),
    path('',include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)