from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import SupportGroup, AnonymousChatSession, AnonymousChatMessage
from .serializers import (
    SupportGroupSerializer, 
    AnonymousChatSessionSerializer, 
    AnonymousChatMessageSerializer
)
from .permissions import IsPatientUser
from users.models import DoctorProfile

# 1. عرض مجموعات الدعم (للكل)
class SupportGroupListView(generics.ListAPIView):
    queryset = SupportGroup.objects.all()
    serializer_class = SupportGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# 2. بدء جلسة دردشة مجهولة (للمريض فقط)
class StartAnonymousChatView(generics.CreateAPIView):
    serializer_class = AnonymousChatSessionSerializer
    permission_classes = [IsPatientUser]

    def perform_create(self, serializer):
        # منطق بسيط: بنختار "أول دكتور متاح" (أو ممكن نخليه عشوائي)
        # في نظام حقيقي ممكن يكون في خوارزمية معقدة
        doctor = DoctorProfile.objects.filter(is_verified=True).first()
        if not doctor:
            # إذا ما في دكاترة، بنعطي خطأ
            raise serializers.ValidationError("لا يوجد أطباء متاحين حالياً.")
            
        serializer.save(
            patient=self.request.user.patient_profile,
            doctor=doctor
        )

# 3. إرسال واستعراض الرسائل (للمريض والدكتور)
class ChatMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = AnonymousChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # بنجيب الجلسة من الرابط (UUID)
        session_id = self.kwargs['session_id']
        return AnonymousChatMessage.objects.filter(session_id=session_id)

    def perform_create(self, serializer):
        session_id = self.kwargs['session_id']
        session = get_object_or_404(AnonymousChatSession, id=session_id)
        
        # تأكد إن المستخدم هو "طرف" في هذه المحادثة
        user = self.request.user
        is_patient = hasattr(user, 'patient_profile') and session.patient == user.patient_profile
        is_doctor = hasattr(user, 'doctor_profile') and session.doctor == user.doctor_profile
        
        if not (is_patient or is_doctor):
             raise permissions.PermissionDenied("غير مسموح لك بالمشاركة في هذه الجلسة.")

        serializer.save(sender=user, session=session)