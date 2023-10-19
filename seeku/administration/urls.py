from django.urls import path, include
from administration import views

urlpatterns = [
    path('publish_object', views.publish_object, name='publish_object'),
    path('publish_object_', views.publish_object_, name ='publish_object_'),
    path('my_objects', views.my_objects, name='my_objects'), 
    path('edit_object/<int:object_id>/', views.edit_object, name='edit_object'),
    path('delete_object/<int:object_id>/', views.delete_object, name='delete_object'),
    path('',include('accounts.urls')),
]