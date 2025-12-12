from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import SponsorshipCase, ExpenseReceipt
from .serializers import (
    SponsorshipCaseSerializer, 
    DonationSerializer, 
    ExpenseReceiptSerializer
)
from .permissions import IsPatientUser, IsDonorUser

# 1. عرض الحالات + إنشاء حالة جديدة
class SponsorshipCaseListCreateView(generics.ListCreateAPIView):
    """
    GET: عرض كل الحالات الموثقة (للجميع).
    POST: مريض يطلب فتح حالة جديدة (للمرضى فقط).
    """
    serializer_class = SponsorshipCaseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsPatientUser()] # بس المريض بيقدر يطلب
        return [permissions.AllowAny()] # الكل بيقدر يتفرج

    def get_queryset(self):
        # بنعرض بس الحالات الموثقة (Verified)
        return SponsorshipCase.objects.filter(is_verified=True)

    def perform_create(self, serializer):
        # بنربط الحالة بالمريض اللي باعت الطلب
        serializer.save(patient=self.request.user.patient_profile)


# 2. عرض تفاصيل حالة واحدة
class SponsorshipCaseDetailView(generics.RetrieveAPIView):
    """
    GET: عرض تفاصيل حالة معينة (مع المبلغ المجمع).
    """
    queryset = SponsorshipCase.objects.filter(is_verified=True)
    serializer_class = SponsorshipCaseSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


# 3. التبرع لحالة (Donate)
class DonationCreateView(generics.CreateAPIView):
    """
    POST: متبرع يقوم بالتبرع لحالة محددة.
    """
    serializer_class = DonationSerializer
    permission_classes = [IsDonorUser] # بس المتبرع بيقدر يدفع

    def create(self, request, *args, **kwargs):
        # (حركة ذكية): بناخد رقم الحالة من الرابط (URL) وبنضيفه للبيانات
        # عشان المتبرع ما يغلب حاله ويكتبه بالـ Body
        case_id = self.kwargs.get('case_id')
        
        # بننسخ البيانات وبنضيف عليها الـ case_id
        data = request.data.copy()
        data['case_id'] = case_id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # بنربط التبرع بالمتبرع الحالي
        serializer.save(donor=self.request.user)


# 4. الشفافية (عرض الفواتير)
class TransparencyReceiptsView(generics.ListAPIView):
    """
    GET: عرض الفواتير والإيصالات الخاصة بحالة معينة.
    """
    serializer_class = ExpenseReceiptSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        case_id = self.kwargs['case_id']
        return ExpenseReceipt.objects.filter(case_id=case_id)