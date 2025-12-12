from django.urls import path
from . import views

urlpatterns = [
    # 1. الحالات (عرض باستخدام Raw SQL Select)
    path('cases/', views.SponsorshipCaseListCreateView.as_view(), name='case-list-create'),

    # 2. الإحصائيات (جديد - باستخدام Raw SQL Aggregation)
    path('analytics/', views.SponsorshipAnalyticsView.as_view(), name='sponsorship-analytics'),

    # 3. الموافقة الطارئة (جديد - باستخدام Raw SQL Update)
    path('emergency-approve/', views.EmergencyApproveView.as_view(), name='emergency-approve'),

    # ... الروابط العادية ...
    path('cases/<int:id>/', views.SponsorshipCaseDetailView.as_view(), name='case-detail'),
    path('cases/<int:case_id>/donate/', views.DonationCreateView.as_view(), name='donate-to-case'),
    path('cases/<int:case_id>/transparency/', views.TransparencyReceiptsView.as_view(), name='case-transparency'),
]