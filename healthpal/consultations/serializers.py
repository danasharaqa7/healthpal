# healthpal/consultations/serializers.py

from rest_framework import serializers
from .models import DoctorAvailabilitySlot, Consultation
from users.models import DoctorProfile, User


class PublicUserDisplaySerializer(serializers.ModelSerializer):
    """
    Serializer (آمن) لعرض بيانات المستخدم "العامة" فقط (الاسم).
    رح نستخدمه جوا DoctorListSerializer.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class DoctorListSerializer(serializers.ModelSerializer):
    """
    Serializer (آمن) لعرض قائمة الأطباء.
    (مطابق لتصميم v2.0 ملف 13، سيريالايزر 2.A)
    """
    user = PublicUserDisplaySerializer(read_only=True)
    languages = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = DoctorProfile
        # هاي بس الحقول "العامة" اللي المريض مسموح يشوفها
        fields = ['user', 'specialty', 'is_international', 'is_verified', 'languages']
        read_only_fields = fields


# --- 2. Serializer لعرض المواعيد المتاحة ---

class DoctorAvailabilitySlotSerializer(serializers.ModelSerializer):
    """
    Serializer لعرض "فتحات" المواعيد المتاحة للدكتور.
    """
    class Meta:
        model = DoctorAvailabilitySlot
        # رح نعرض بس المواعيد (is_booked = False)
        fields = ['id', 'start_time', 'end_time']
        read_only_fields = fields


# --- 3. Serializer لحجز وعرض الاستشارة (الأهم) ---

class ConsultationSerializer(serializers.ModelSerializer):
    """
    Serializer لحجز (POST) وعرض (GET) الاستشارة.
    """
    
    # --- حقول العرض (Read-only) ---
    # (v2.0) لما نعرض "موعد"، بنعرض بيانات المريض والدكتور كاملة (Nested)
    patient = PublicUserDisplaySerializer(read_only=True, source='patient.user')
    doctor = DoctorListSerializer(read_only=True)
    status = serializers.CharField(read_only=True, default=Consultation.ConsultationStatus.BOOKED)
    
    # --- حقول الحجز (Write-only) ---
    # (v2.0) المريض بس ببعتلنا "رقم" الـ Slot اللي بده يحجزه
    availability_slot_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 
            'patient', 
            'doctor', 
            'status', 
            'consultation_type', # (رح نقرأها من الحجز)
            'availability_slot_id' # (رح نستخدمها بس للحجز)
        ]
        
    def validate(self, data):
        """
        (v2.0) التأكد من صلاحية الحجز (Validation).
        """
        slot_id = data.get('availability_slot_id')
        try:
            slot = DoctorAvailabilitySlot.objects.get(id=slot_id)
        except DoctorAvailabilitySlot.DoesNotExist:
            raise serializers.ValidationError("هذا الموعد (Slot) غير موجود.")

        # (v2.0) نتأكد إنه الموعد مش محجوز
        if slot.is_booked:
            raise serializers.ValidationError("عذراً، هذا الموعد تم حجزه للتو.")
            
        data['slot_object'] = slot # بنخزن الـ object عشان نستخدمه بالـ create
        return data

    def create(self, validated_data):
        """
        إنشاء الحجز (Booking).
        """
        # بنجيب الـ Slot اللي تأكدنا إنه موجود ومش محجوز
        slot = validated_data.pop('slot_object')
        
        patient_profile = self.context['request'].user.patient_profile

        # 1. بننشئ الموعد (Consultation)
        consultation = Consultation.objects.create(
            patient=patient_profile,
            doctor=slot.doctor, # الدكتور صاحب الـ Slot
            availability_slot=slot,
            consultation_type=validated_data.get('consultation_type', Consultation.ConsultationType.VIDEO)
        )

        # 2. (الأهم) بنحدّث الـ Slot وبنخليه "محجوز"
        slot.is_booked = True
        slot.save()

        return consultation