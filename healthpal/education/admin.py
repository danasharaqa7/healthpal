from django.contrib import admin
from .models import HealthGuide, HealthAlert, Webinar

class HealthGuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_visual', 'created_at')
    list_filter = ('category', 'is_visual')
    search_fields = ('title',)

class HealthAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'is_active', 'created_at')
    list_filter = ('severity', 'is_active')

class WebinarAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'date_time')

admin.site.register(HealthGuide, HealthGuideAdmin)
admin.site.register(HealthAlert, HealthAlertAdmin)
admin.site.register(Webinar, WebinarAdmin)