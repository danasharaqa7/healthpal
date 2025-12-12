from django.contrib import admin
from .models import NGO, MedicalMission

class NGOAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('name',)

class MedicalMissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'ngo', 'mission_type', 'start_date', 'location')
    list_filter = ('mission_type', 'start_date')
    search_fields = ('title', 'location', 'specialties_available')

admin.site.register(NGO, NGOAdmin)
admin.site.register(MedicalMission, MedicalMissionAdmin)