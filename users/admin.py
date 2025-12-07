from django.contrib import admin
from .models import User, Role, UserRole, PatientProfile, DoctorProfile, Language

# تحسين عرض المستخدمين
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')

# تحسين عرض البروفايلات
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'is_verified', 'is_international')
    list_filter = ('is_verified', 'is_international', 'specialty')
    search_fields = ('user__email', 'specialty')

# تسجيل الموديلز
admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Language)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile, DoctorProfileAdmin)