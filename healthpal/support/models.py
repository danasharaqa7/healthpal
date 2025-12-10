import uuid
from django.db import models
from django.conf import settings
from users.models import PatientProfile, DoctorProfile

class SupportGroup(models.Model):
    """
    مجموعات الدعم النفسي (مثل: دعم الصدمات، الفقدان).
    يديرها طبيب أو مشرف.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    # المشرف على المجموعة (دكتور)
    moderator = models.ForeignKey(
        DoctorProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='moderated_groups'
    )
    
    # رابط اللقاء (إذا كان أونلاين)
    meeting_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AnonymousChatSession(models.Model):
    """
    جلسة دردشة سرية بين مريض وطبيب.
    نستخدم UUID بدل الأرقام العادية (1, 2, 3) لزيادة الخصوصية وصعوبة التخمين.
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ENDED', 'Ended'),
    ]

    # المفتاح الرئيسي هو رمز عشوائي طويل (UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # النظام بيعرف مين المريض، بس ما بنعرض اسمه في الـ API العام
    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name='chat_sessions'
    )
    
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='chat_sessions'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {str(self.id)[:8]}..."


class AnonymousChatMessage(models.Model):
    """
    الرسائل داخل الجلسة السرية.
    """
    session = models.ForeignKey(
        AnonymousChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    # مين اللي بعت؟ (عشان نعرف نعرض الرسالة يمين ولا يسار)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] # ترتيب الرسائل حسب الوقت

    def __str__(self):
        return f"Message in {str(self.session.id)[:8]}"