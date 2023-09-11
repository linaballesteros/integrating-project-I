from django.urls import path
from . import views
urlpatterns = [
    path('filtered/',views.filterObjects, name='filter'),
]
