from django.db import models
from django.conf import settings

class NGO(models.Model):
    """
    المنظمات غير الحكومية الموثقة (Verified NGO Network).
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    
    # هل المنظمة موثقة من قبل النظام؟
    is_verified = models.BooleanField(default=False)
    
    logo = models.URLField(blank=True, null=True) # رابط لشعار المنظمة
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MedicalMission(models.Model):
    """
    البعثات الطبية والحملات الجراحية (Surgical Missions Tracker).
    """
    MISSION_TYPES = [
        ('SURGERY', 'Surgery Camp'),
        ('MOBILE_CLINIC', 'Mobile Clinic'),
        ('TRAINING', 'Medical Training'),
        ('FIELD_HOSPITAL', 'Field Hospital'),
    ]

    title = models.CharField(max_length=255) # e.g., "مخيم جراحة العيون - غزة"
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name='missions')
    mission_type = models.CharField(max_length=50, choices=MISSION_TYPES)
    
    description = models.TextField()
    location = models.CharField(max_length=255) # وين رح تكون البعثة؟
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    # التخصصات المتاحة في هذه البعثة (JSON or Text)
    specialties_available = models.TextField(help_text="e.g., Orthopedics, Ophthalmology")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.start_date})"