from rest_framework import permissions

class IsDonorUser(permissions.BasePermission):
    """
    صلاحية مخصصة للتأكد أن المستخدم هو "متبرع" (Donor).
    """
    message = 'فقط المستخدمين بصلاحية "متبرع" (Donor) يمكنهم تنفيذ هذا الإجراء.'

    def has_permission(self, request, view):
        # 1. هل هو مسجل دخول؟
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 2. هل يمتلك صلاحية DONOR؟
        # (بما أننا استخدمنا Many-to-Many، نفحص إذا كان لديه الصلاحية)
        return request.user.user_roles.filter(role__name='DONOR').exists()

class IsPatientUser(permissions.BasePermission):
    """
    (نسخة للمريض هنا أيضاً لاستخدامها في طلب الكفالة)
    """
    message = 'فقط المستخدمين بصلاحية "مريض" (Patient) يمكنهم فتح حالة كفالة.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'patient_profile')