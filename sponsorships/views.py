from django.db import connection  # (أهم استيراد للـ Raw SQL)
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SponsorshipCase, ExpenseReceipt
from .serializers import (
    SponsorshipCaseSerializer, 
    DonationSerializer, 
    ExpenseReceiptSerializer
)
from .permissions import IsPatientUser, IsDonorUser

# --- مثال 1: SELECT (استرجاع بيانات) ---
class SponsorshipCaseListCreateView(generics.ListCreateAPIView):
    serializer_class = SponsorshipCaseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsPatientUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        # [RAW SQL DEMO]: استرجاع الحالات الموثقة فقط
        # نستخدم raw() عشان ترجع النتيجة كـ Objects ونقدر نعرضها بالـ Serializer
        sql = "SELECT * FROM sponsorships_sponsorshipcase WHERE is_verified = %s"
        return SponsorshipCase.objects.raw(sql, [1])

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient_profile)


# --- مثال 2: AGGREGATION (حسابات وأرقام) ---
class SponsorshipAnalyticsView(APIView):
    """
    Endpoint جديد لعرض إحصائيات النظام باستخدام SQL مباشر.
    (يستخدم cursor.execute لأنه ما بنرجع Model، بنرجع أرقام بس).
    """
    permission_classes = [permissions.AllowAny] # متاح للكل عشان يشوفوا الخير

    def get(self, request):
        with connection.cursor() as cursor:
            # 1. حساب مجموع التبرعات الكلي
            cursor.execute("SELECT SUM(amount) FROM sponsorships_donation")
            total_donations = cursor.fetchone()[0] or 0

            # 2. عد الحالات المكتملة (FULLY_FUNDED)
            cursor.execute("SELECT COUNT(*) FROM sponsorships_sponsorshipcase WHERE status = %s", ['FULLY_FUNDED'])
            completed_cases = cursor.fetchone()[0]

        return Response({
            "total_donations_collected": total_donations,
            "cases_fully_funded": completed_cases,
            "message": "These stats were calculated using Raw SQL Queries."
        })


# --- مثال 3: UPDATE (تعديل بيانات) ---
class EmergencyApproveView(APIView):
    """
    Endpoint للطوارئ: يقوم بالموافقة (Verify) على كل الحالات "الجراحية" (SURGERY) دفعة واحدة.
    (مثال قوي على جملة UPDATE).
    """
    permission_classes = [permissions.IsAdminUser] # للأدمن فقط

    def post(self, request):
        with connection.cursor() as cursor:
            # جملة SQL لتحديث عدة أسطر مرة واحدة
            sql = """
                UPDATE sponsorships_sponsorshipcase 
                SET is_verified = 1 
                WHERE treatment_type = %s AND is_verified = 0
            """
            cursor.execute(sql, ['SURGERY'])
            rows_affected = cursor.rowcount # كم سطر تعدل؟

        return Response({
            "status": "success",
            "cases_approved_count": rows_affected,
            "message": f"Successfully auto-verified {rows_affected} surgery cases using Raw SQL."
        })


# --- باقي الـ Views العادية (ما غيرنا عليها شي) ---

class SponsorshipCaseDetailView(generics.RetrieveAPIView):
    queryset = SponsorshipCase.objects.filter(is_verified=True)
    serializer_class = SponsorshipCaseSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

class DonationCreateView(generics.CreateAPIView):
    serializer_class = DonationSerializer
    permission_classes = [IsDonorUser]

    def create(self, request, *args, **kwargs):
        case_id = self.kwargs.get('case_id')
        data = request.data.copy()
        data['case_id'] = case_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

class TransparencyReceiptsView(generics.ListAPIView):
    serializer_class = ExpenseReceiptSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        case_id = self.kwargs['case_id']
        return ExpenseReceipt.objects.filter(case_id=case_id)