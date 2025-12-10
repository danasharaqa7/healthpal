from django.urls import path
from . import views

urlpatterns = [
    # 1. الحالات (عرض الكل + إنشاء جديد)
    # GET /api/v1/sponsorship/cases/
    # POST /api/v1/sponsorship/cases/
    path('cases/', views.SponsorshipCaseListCreateView.as_view(), name='case-list-create'),

    # 2. تفاصيل حالة واحدة
    # GET /api/v1/sponsorship/cases/{id}/
    path('cases/<int:id>/', views.SponsorshipCaseDetailView.as_view(), name='case-detail'),

    # 3. التبرع لحالة
    # POST /api/v1/sponsorship/cases/{id}/donate/
    path('cases/<int:case_id>/donate/', views.DonationCreateView.as_view(), name='donate-to-case'),

    # 4. الشفافية (الفواتير)
    # GET /api/v1/sponsorship/cases/{id}/transparency/
    path('cases/<int:case_id>/transparency/', views.TransparencyReceiptsView.as_view(), name='case-transparency'),
]