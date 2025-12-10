from rest_framework import serializers
from .models import SupportGroup, AnonymousChatSession, AnonymousChatMessage
from users.serializers import DoctorProfileSerializer
from consultations.serializers import DoctorListSerializer

class SupportGroupSerializer(serializers.ModelSerializer):
    """
    عرض مجموعات الدعم.
    """
    moderator_name = serializers.CharField(source='moderator.user.last_name', read_only=True)

    class Meta:
        model = SupportGroup
        fields = ['id', 'name', 'description', 'moderator_name', 'meeting_link', 'created_at']


class AnonymousChatSessionSerializer(serializers.ModelSerializer):
    """
    بدء جلسة دردشة جديدة.
    """
    # بنعرض بيانات الدكتور للمريض
    doctor = DoctorListSerializer(read_only=True)
    
    # بنرجع رقم الجلسة (UUID) عشان يستخدمه في إرسال الرسائل
    session_id = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = AnonymousChatSession
        fields = ['session_id', 'doctor', 'status', 'created_at']


class AnonymousChatMessageSerializer(serializers.ModelSerializer):
    """
    إرسال واستقبال الرسائل.
    """
    # حقل ذكي بيحكيلنا مين اللي بعت الرسالة (مريض ولا دكتور)
    sender_role = serializers.SerializerMethodField()

    class Meta:
        model = AnonymousChatMessage
        fields = ['id', 'content', 'timestamp', 'sender_role']

    def get_sender_role(self, obj):
        # بنشيك: هل المرسل هو صاحب الجلسة (المريض)؟
        if obj.sender == obj.session.patient.user:
            return 'PATIENT'
        return 'DOCTOR'