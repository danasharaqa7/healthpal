# healthpal/consultations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # --- (جديد) روابط الـ Doctors ---
    
    # GET /api/v1/doctors/
    # (لعرض قائمة كل الدكاترة الموثقين)
    path('doctors/', views.DoctorListView.as_view(), name='doctor-list'),
    
    # GET /api/v1/doctors/<id>/availability/
    # (لعرض المواعيد المتاحة لدكتور معين)
    path('doctors/<int:doctor_id>/availability/', views.DoctorAvailabilityListView.as_view(), name='doctor-availability'),

    # --- (جديد) روابط الـ Consultations ---
    
    # GET /api/v1/consultations/
    # (لعرض "مواعيدي" (كمريض أو كدكتور))
    # POST /api/v1/consultations/
    # (لحجز موعد جديد (كمريض))
    path('consultations/', views.ConsultationListCreateView.as_view(), name='consultation-list-create'),
]