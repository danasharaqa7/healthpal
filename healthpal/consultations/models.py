# healthpal/consultations/models.py
# (النسخة المصححة والنهائية 100%)

from django.db import models
from django.conf import settings

# --- (مهم جداً) استيراد الموديلز اللي بنحتاجها من تطبيق users ---
# إحنا بحاجة لملفات الـ Profiles عشان نربط فيهم
from users.models import PatientProfile, DoctorProfile

# --- 1. جدول فتحات المواعيد المتاحة (جدول 8 في تصميم v2.0) ---
# (هاد هو الجدول المفقود اللي ضفناه في v2.0)
class DoctorAvailabilitySlot(models.Model):
    """
    يخزن "فتحات" المواعيد المتاحة التي يحددها الطبيب.
    (مطابق لجدول 8 في ملف تصميم الداتابيز v2.0)
    """
    # الربط مع الدكتور (كل دكتور عنده "عدة" مواعيد متاحة)
    doctor = models.ForeignKey(
        DoctorProfile, 
        on_delete=models.CASCADE, 
        related_name='availability_slots'
    )     
    
    start_time = models.DateTimeField() # e.g., "2025-11-10 09:00:00"
    end_time = models.DateTimeField()   # e.g., "2025-11-10 09:30:00"
    
    # هل هاد الموعد انحجز؟
    is_booked = models.BooleanField(default=False)

    class Meta:
        # بنضمن إنه ما في موعدين بنفس الوقت لنفس الدكتور
        unique_together = ('doctor', 'start_time', 'end_time')
        ordering = ['start_time'] # بنرتبهم دايماً حسب وقت البداية

    def __str__(self):
        return f"Dr. {self.doctor.user.last_name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


# --- 2. جدول الاستشارة (جدول 9 في تصميم v2.0) ---
# (هاد هو جدول "الحجز" الفعلي)
class Consultation(models.Model):
    """
    يخزن "موعد" (booking) بين مريض وطبيب في فتحة زمنية محددة.
    (مطابق لجدول 9 في ملف تصميم الداتابيز v2.0)
    """
    
    # تعريف الحالات (Status)
    class ConsultationStatus(models.TextChoices):
        BOOKED = 'BOOKED', 'Booked'         # محجوز
        COMPLETED = 'COMPLETED', 'Completed' # مكتمل
        CANCELLED = 'CANCELLED', 'Cancelled' # ملغي
    
    # تعريف نوع الاستشارة (Low-Bandwidth Mode)
    class ConsultationType(models.TextChoices):
        VIDEO = 'VIDEO', 'Video Call'               # (افتراضي)
        AUDIO_ONLY = 'AUDIO_ONLY', 'Audio Only'     # (للاتصال الضعيف)
        MESSAGING = 'MESSAGING', 'Asynchronous Messaging' # (للاتصال الضعيف)

    # --- العلاقات (الربط) ---
    
    # مين المريض؟
    patient = models.ForeignKey(
        PatientProfile, 
        on_delete=models.SET_NULL, # (إذا انحذف المريض، الموعد بضل موجود بس بدون مريض)
        null=True,
        related_name='consultations'
    )
    
    # مين الدكتور؟
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.SET_NULL, # (إذا انحذف الدكتور، الموعد بضل)
        null=True,
        related_name='consultations'
    )

    # (v2.0) الحجز مربوط بـ "فتحة" موعد محددة
    # (استخدمنا OneToOne عشان نضمن إنه الـ Slot الواحد بنحجز "مرة واحدة" بس)
    availability_slot = models.OneToOneField(
        DoctorAvailabilitySlot,
        on_delete=models.SET_NULL, # (إذا انحذف الـ Slot، الموعد بضل)
        null=True,
        related_name='consultation'
    )

    # --- باقي البيانات ---
    
    status = models.CharField(
        max_length=20,
        choices=ConsultationStatus.choices,
        default=ConsultationStatus.BOOKED
    )
    
    consultation_type = models.CharField(
        max_length=20,
        choices=ConsultationType.choices,
        default=ConsultationType.VIDEO
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation {self.id} ({self.status}) - Patient: {self.patient.user.last_name} with Dr. {self.doctor.user.last_name}"