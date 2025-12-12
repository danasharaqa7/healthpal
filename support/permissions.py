from rest_framework import permissions

class IsPatientUser(permissions.BasePermission):
    """
    صلاحية مخصصة للتأكد أن المستخدم هو "مريض".
    """
    message = 'فقط المستخدمين بصلاحية "مريض" (Patient) يمكنهم تنفيذ هذا الإجراء.'

    def has_permission(self, request, view):
        # 1. هل هو مسجل دخول؟
        if not request.user or not request.user.is_authenticated:
            return False
        # 2. هل عنده "ملف مريض"؟
        return hasattr(request.user, 'patient_profile')