from django.contrib import admin
from .models import SupportGroup, AnonymousChatSession, AnonymousChatMessage

class AnonymousChatMessageInline(admin.TabularInline):
    model = AnonymousChatMessage
    extra = 0
    readonly_fields = ('sender', 'timestamp')

class AnonymousChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'status', 'created_at')
    inlines = [AnonymousChatMessageInline] # عشان نشوف الرسائل جوا الجلسة

admin.site.register(SupportGroup)
admin.site.register(AnonymousChatSession, AnonymousChatSessionAdmin)