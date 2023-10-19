from django.urls import path, include
from analytics import views
from django.conf.urls.static import static
from django.conf import settings
from app import views as seek_Uviews

urlpatterns = [
    path("search/", seek_Uviews.search, name = 'search'),
    path("claim_request/", seek_Uviews.claim_request, name = 'claim_request'),
    path('history/', seek_Uviews.history, name='history'),
    path('claim/',seek_Uviews.ClaimObjectView.as_view(),name="claim_req"),
    path('claim/filtered/',seek_Uviews.filterObjects, name='filter'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)