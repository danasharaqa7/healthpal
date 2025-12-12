from django.contrib import admin
from .models import SponsorshipCase, Donation, ExpenseReceipt

class SponsorshipCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'donation_goal', 'current_donated_amount', 'is_verified', 'status')
    list_filter = ('is_verified', 'status', 'treatment_type')
    search_fields = ('title', 'patient__user__email')

class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'case', 'amount', 'timestamp')
    list_filter = ('timestamp',)

class ExpenseReceiptAdmin(admin.ModelAdmin):
    list_display = ('case', 'description', 'created_at')

admin.site.register(SponsorshipCase, SponsorshipCaseAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(ExpenseReceipt, ExpenseReceiptAdmin)