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
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', seek_Uviews.home),
    path('register', seek_Uviews.register_user),
    path("search/", seek_Uviews.search),
    path("claim_request/", seek_Uviews.claim_request, name = 'claim_request'),
    path('login', seek_Uviews.login, name='login'),
]

