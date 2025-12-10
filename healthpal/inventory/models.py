from django.db import models
from django.conf import settings
from users.models import PatientProfile

class MedicalItem(models.Model):
    """
    جدول تعريفي لكل الأدوية والمعدات الممكنة في النظام.
    (e.g., Panadol, Wheelchair, Oxygen Tank)
    """
    ITEM_TYPES = [
        ('MEDICINE', 'Medicine'),
        ('EQUIPMENT', 'Medical Equipment'),
    ]

    name = models.CharField(max_length=255, unique=True) # اسم الدواء/المعدة
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_item_type_display()})"


class InventoryItem(models.Model):
    """
    المخزون المتاح (Surplus) الذي يعرضه المتبرعون أو الموزعون.
    """
    # المتبرع/الموزع (صيدلية، مستشفى، أو شخص)
    distributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventory_items'
    )
    
    item = models.ForeignKey(MedicalItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField() # الكمية المتاحة
    expiry_date = models.DateField(blank=True, null=True) # مهم للأدوية
    location = models.CharField(max_length=255) # وين الغرض موجود؟
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - Qty: {self.quantity}"


class ItemRequest(models.Model):
    """
    طلبات المرضى للأدوية أو المعدات.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),       # بانتظار الموافقة/التوصيل
        ('FULFILLED', 'Fulfilled'),   # تم التوفير (لقينا المتبرع)
        ('DELIVERED', 'Delivered'),   # وصل للمريض
        ('CANCELLED', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name='item_requests'
    )
    
    # المادة المطلوبة
    item = models.ForeignKey(MedicalItem, on_delete=models.CASCADE)
    quantity_needed = models.PositiveIntegerField(default=1)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # مين موظف الـ NGO اللي لبى الطلب؟ (اختياري)
    fulfilled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fulfilled_requests'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request: {self.item.name} for {self.patient.user.last_name}"