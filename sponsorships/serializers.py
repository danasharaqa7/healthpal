from rest_framework import serializers
from .models import SponsorshipCase, Donation, ExpenseReceipt
from users.serializers import UserDisplaySerializer

# (v2.0) استيراد السيريالايزر العام للمريض عشان الخصوصية
# (ملاحظة: لازم نضيف PublicPatientProfileSerializer في users/serializers.py أولاً إذا مش موجود)
# للتبسيط الآن سنستخدم UserDisplaySerializer، ولكن الأصح استخدام PublicPatientProfileSerializer
# سنقوم بتعريفه هنا مؤقتاً أو نستخدم الموجود.

class SponsorshipCaseSerializer(serializers.ModelSerializer):
    """
    Serializer لعرض وإنشاء حالات الكفالة.
    """
    # بنعرض بيانات المريض (للقراءة فقط)
    patient = UserDisplaySerializer(source='patient.user', read_only=True)
    
    # حقول محسوبة أو للقراءة فقط
    current_donated_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = SponsorshipCase
        fields = [
            'id', 'patient', 'title', 'treatment_type', 'description',
            'donation_goal', 'current_donated_amount', 
            'is_verified', 'status', 'created_at'
        ]


class DonationSerializer(serializers.ModelSerializer):
    """
    Serializer للتبرع (Donation).
    """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    donor = UserDisplaySerializer(read_only=True)
    
    # (Write-only) رقم الحالة اللي بدنا نتبرع الها
    case_id = serializers.IntegerField(write_only=True, required=True)
    
    # (Read-only) تفاصيل الحالة للعرض
    case = SponsorshipCaseSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'amount', 'donor', 'case_id', 'case', 'timestamp']

    def validate_amount(self, value):
        """
        (v2.0) التأكد أن المبلغ موجب.
        """
        if value <= 0:
            raise serializers.ValidationError("مبلغ التبرع يجب أن يكون أكبر من صفر.")
        return value

    def create(self, validated_data):
        """
        تنفيذ التبرع وتحديث رصيد الحالة.
        """
        case_id = validated_data.pop('case_id')
        try:
            case = SponsorshipCase.objects.get(id=case_id)
        except SponsorshipCase.DoesNotExist:
            raise serializers.ValidationError("الحالة غير موجودة.")

        # إنشاء التبرع
        donation = Donation.objects.create(case=case, **validated_data)

        # تحديث الرصيد في جدول الحالة
        case.current_donated_amount += donation.amount
        
        # (Logic) إذا اكتمل المبلغ، نغير الحالة لـ FULLY_FUNDED
        if case.current_donated_amount >= case.donation_goal:
            case.status = 'FULLY_FUNDED'
        
        case.save()
        return donation


class ExpenseReceiptSerializer(serializers.ModelSerializer):
    """
    Serializer لعرض إيصالات الشفافية.
    """
    class Meta:
        model = ExpenseReceipt
        fields = '__all__'
        