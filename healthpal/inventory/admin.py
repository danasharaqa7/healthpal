from django.contrib import admin
from .models import MedicalItem, InventoryItem, ItemRequest

class MedicalItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type')
    search_fields = ('name',)
    list_filter = ('item_type',)

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'distributor', 'quantity', 'expiry_date', 'location')
    list_filter = ('item__item_type', 'expiry_date')
    search_fields = ('item__name', 'distributor__email')

class ItemRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'item', 'quantity_needed', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__user__email', 'item__name')

admin.site.register(MedicalItem, MedicalItemAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(ItemRequest, ItemRequestAdmin)