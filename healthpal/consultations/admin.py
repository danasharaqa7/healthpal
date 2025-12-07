from django.contrib import admin
from .models import DoctorAvailabilitySlot, Consultation

class DoctorAvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_time', 'end_time', 'is_booked')
    list_filter = ('is_booked', 'start_time')
    ordering = ('start_time',)

class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'status', 'created_at')
    list_filter = ('status', 'consultation_type')

admin.site.register(DoctorAvailabilitySlot, DoctorAvailabilitySlotAdmin)
admin.site.register(Consultation, ConsultationAdmin)