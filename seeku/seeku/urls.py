"""
URL configuration for seeku project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views as seek_Uviews

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', seek_Uviews.home, name = 'home_aferlogin'),
    path('register', seek_Uviews.register_user),
    path("search/", seek_Uviews.search, name = 'search'),
    path("claim_request/", seek_Uviews.claim_request, name = 'claim_request'),
    path('login', seek_Uviews.login, name='login'),
    path('my_profile', seek_Uviews.my_profile, name='my_profile'),
    path('history/', seek_Uviews.history, name='history'),
    path('edit_profile_view/', seek_Uviews.edit_profile_view, name='edit_profile_view'),
    path('about/', seek_Uviews.about, name='_about'),
    path('analytics/', seek_Uviews.analytics, name='_analytics'),
    path('publish_object', seek_Uviews.publish_object, name='publish_object'), # html, 
    path('publish_object_', seek_Uviews.publish_object_, name='publish_object_'), # specific request when submitting an object to django admin
    path('my_objects', seek_Uviews.my_objects, name='my_objects'), 
  #  path('edit_object', seek_Uviews.edit_object, name='edit_object'), 
    path('edit_object/<int:object_id>/', seek_Uviews.edit_object, name='edit_object'),
    path('claim/',seek_Uviews.ClaimObjectView.as_view(),name="claim_req"),
    path('claim/filtered/',seek_Uviews.filterObjects, name='filter'),
    path('delete_object/<int:object_id>/', seek_Uviews.delete_object, name='delete_object'),
    path('Path.html', seek_Uviews.map_view, name='map_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

