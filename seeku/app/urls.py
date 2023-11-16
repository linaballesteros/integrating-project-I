from django.urls import path, include
from analytics import views
from django.conf.urls.static import static
from django.conf import settings
from app import views as seek_Uviews
from menu import views

urlpatterns = [
    path("search/", seek_Uviews.search, name = 'search'),
    path("search_es/", seek_Uviews.search_es, name = 'search'),
    path("claim_request/", seek_Uviews.claim_request, name = 'claim_request'),
    path('history/', seek_Uviews.history, name='history'),
    path('history_es/', seek_Uviews.history_es, name='history_es'),
    path('claim/',seek_Uviews.ClaimObjectView.as_view(),name="claim_req"),
    path('claim_es/',seek_Uviews.ClaimObjectView_es.as_view(),name="claim_req_es"),
    path('claim/filtered/',seek_Uviews.filterObjects, name='filter'),
    path('claim/filtered_es/',seek_Uviews.filterObjects_es, name='filter_es'),
    path('claim/notify/',seek_Uviews.NotifyMe,name="notify"),
    path('claiming<id>',seek_Uviews.claiming,name="claiming"),
    path('claim/complaint/<id>/<int:method>',seek_Uviews.claim_complaint,name="complaint"),
    path('claim/complaints/view/', seek_Uviews.claim_complaints_views,name='claim_complaints_view'),
    path('claim/complaints/view/<id>',seek_Uviews.claim_complaint_detail_view,name='claim_complaint_detail'),
    path('claim/complaints/script/<id>/<user_email>/<int:parametro>',seek_Uviews.claim_complaint_script,name='claim_complaint_script')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)