# healthpal/consultations/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import DoctorAvailabilitySlot, Consultation
from users.models import DoctorProfile
from .serializers import (
    DoctorListSerializer, 
    DoctorAvailabilitySlotSerializer, 
    ConsultationSerializer
)
# (جديد) رح نستورد الصلاحيات المخصصة اللي عملناها
from .permissions import IsPatientUser, IsDoctorUser

# --- Endpoints لعرض معلومات الدكاترة (للكل) ---

class DoctorListView(generics.ListAPIView):
    """
    View لعرض "قائمة كل" الأطباء الموثقين.
    (Endpoint: GET /api/v1/doctors)
    (مطابق لتصميم v2.0 ملف 12)
    """
    # (v2.0) إحنا بنعرض بس الدكاترة الموثقين (Verified)
    queryset = DoctorProfile.objects.filter(is_verified=True)
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.AllowAny] # أي حدا (حتى الزوار) بقدر يشوف الدكاترة


class DoctorAvailabilityListView(generics.ListAPIView):
    """
    View لعرض "المواعيد المتاحة" (Slots) لدكتور معين.
    (Endpoint: GET /api/v1/doctors/{id}/availability)
    (مطابق لتصميم v2.0 ملف 12)
    """
    serializer_class = DoctorAvailabilitySlotSerializer
    permission_classes = [permissions.IsAuthenticated] # لازم يكون مسجل دخول عشان يشوف المواعيد

    def get_queryset(self):
        """
        هاي الـ function بتفلتر المواعيد بناءً على "رقم الدكتور" (id)
        اللي إجا بالـ URL.
        """
        # بنجيب الـ id تاع الدكتور من الـ URL
        doctor_id = self.kwargs['doctor_id']
        
        # (v2.0) بنجيب "فقط" المواعيد اللي "مش محجوزة"
        return DoctorAvailabilitySlot.objects.filter(
            doctor_id=doctor_id,
            is_booked=False
        )

# --- Endpoints لإدارة الاستشارات (للمرضى والدكاترة) ---

class ConsultationListCreateView(generics.ListCreateAPIView):
    """
    View لـ "عرض مواعيدي" (GET) أو "حجز موعد جديد" (POST).
    (Endpoint: GET/POST /api/v1/consultations)
    (مطابق لتصميم v2.0 ملف 12)
    """
    serializer_class = ConsultationSerializer
    
    def get_permissions(self):
        """
        هاي الـ function بتحدد الصلاحيات حسب نوع الطلب (GET أو POST)
        """
        if self.request.method == 'POST':
            # "بس المريض" (Patient) بقدر يعمل "حجز" (POST)
            return [IsPatientUser()]
        # أي حدا مسجل دخول (مريض أو دكتور) بقدر "يشوف مواعيده" (GET)
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        هاي الـ function بتجيب "مواعيدي أنا بس".
        """
        user = self.request.user
        if hasattr(user, 'patient_profile'):
            # إذا أنا "مريض"، جيب مواعيدي كمريض
            return Consultation.objects.filter(patient=user.patient_profile)
        elif hasattr(user, 'doctor_profile'):
            # إذا أنا "دكتور"، جيب مواعيدي كدكتور
            return Consultation.objects.filter(doctor=user.doctor_profile)
        return Consultation.objects.none() # إذا لا هاد ولا هاد، رجع "فاضي"

    def perform_create(self, serializer):
        """
        هاي الـ function بتنبعت "قبل" ما الحجز ينعمل.
        بنستخدمها عشان نبعت الـ "request" (اللي فيه الـ user) للـ Serializer.
        """
        # (v2.0) بنبعت الـ request للـ Serializer عشان الـ Serializer
        # يقدر يجيب المريض (Patient) من الـ Token (زي ما برمجناه بالـ Serializer)
        serializer.save(request=self.request)