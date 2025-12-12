from django.db import models
from users.models import PatientProfile, User

class SponsorshipCase(models.Model):
    """
    حالة الكفالة التي يطلبها المريض (مثل عملية جراحية، علاج سرطان).
    (مطابق لجدول 10 في تصميم v2.0)
    """
    TREATMENT_TYPES = [
        ('SURGERY', 'Surgery'),
        ('CANCER', 'Cancer Treatment'),
        ('DIALYSIS', 'Dialysis'),
        ('MEDICATION', 'Chronic Medication'),
        ('REHAB', 'Physical Rehabilitation'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved & Fundraising'),
        ('FULLY_FUNDED', 'Fully Funded'),
        ('COMPLETED', 'Treatment Completed'),
        ('REJECTED', 'Rejected'),
    ]

    # المريض صاحب الحالة
    patient = models.ForeignKey(
        PatientProfile, 
        on_delete=models.CASCADE, 
        related_name='sponsorship_cases'
    )
    
    title = models.CharField(max_length=255) # e.g., "عملية قلب مفتوح"
    treatment_type = models.CharField(max_length=50, choices=TREATMENT_TYPES)
    description = models.TextField() # قصة المريض
    
    # الأمور المالية
    donation_goal = models.DecimalField(max_digits=10, decimal_places=2) # المبلغ المطلوب
    current_donated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # الإدارة
    is_verified = models.BooleanField(default=False) # موافقة الأدمن
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.patient.user.first_name}"


class Donation(models.Model):
    """
    سجل التبرعات المالية لكل حالة.
    (مطابق لجدول 11 في تصميم v2.0)
    """
    # المتبرع (يمكن أن يكون مجهولاً، لكن في نظامنا يجب أن يسجل دخول)
    donor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='donations'
    )
    
    case = models.ForeignKey(
        SponsorshipCase, 
        on_delete=models.CASCADE, 
        related_name='donations'
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} to {self.case.title}"


class ExpenseReceipt(models.Model):
    """
    إيصالات المصاريف لضمان الشفافية (أين ذهبت الأموال؟).
    (مطابق لجدول 12 في تصميم v2.0)
    """
    case = models.ForeignKey(
        SponsorshipCase, 
        on_delete=models.CASCADE, 
        related_name='expenses'
    )
    
    description = models.CharField(max_length=255) # e.g., "فاتورة المستشفى الاستشاري"
    receipt_url = models.URLField() # رابط صورة الفاتورة (أو ملف)
    patient_feedback = models.TextField(blank=True, null=True) # رسالة شكر من المريض
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt for {self.case.title}"