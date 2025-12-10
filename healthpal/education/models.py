from django.db import models
from django.conf import settings

class HealthGuide(models.Model):
    """
    أدلة صحية وتثقيفية (مقالات).
    """
    CATEGORY_CHOICES = [
        ('NUTRITION', 'Nutrition'),
        ('MATERNAL', 'Maternal Care'),
        ('CHRONIC', 'Chronic Diseases'),
        ('FIRST_AID', 'First Aid'),
        ('MENTAL', 'Mental Health'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField() # نص المقال
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    # هل المقال "مرئي"؟ (فيديو أو صورة)
    is_visual = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HealthAlert(models.Model):
    """
    إنذارات صحية عاجلة (مثل تفشي أمراض).
    """
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='MEDIUM')
    location = models.CharField(max_length=255, blank=True, null=True) # هل الإنذار لمنطقة محددة؟
    is_active = models.BooleanField(default=True) # هل الإنذار ما زال سارياً؟
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_severity_display()}] {self.title}"


class Webinar(models.Model):
    """
    ندوات وورشات عمل أونلاين.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    speaker = models.CharField(max_length=255) # اسم المحاضر
    
    date_time = models.DateTimeField()
    meeting_link = models.URLField() # رابط الزووم أو الميتنج
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Webinar: {self.title} on {self.date_time}"