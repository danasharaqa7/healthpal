from rest_framework import permissions

class IsDistributorUser(permissions.BasePermission):
    """
    يسمح فقط للموزعين (Distributors) بإضافة مخزون.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # نفحص إذا عنده صلاحية DISTRIBUTOR
        return request.user.user_roles.filter(role__name='DISTRIBUTOR').exists()

class IsNGOStaffUser(permissions.BasePermission):
    """
    يسمح فقط لموظفي الـ NGO برؤية الطلبات وتلبيتها.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.user_roles.filter(role__name='NGO_STAFF').exists()

class IsPatientUser(permissions.BasePermission):
    """
    (نسخة للمريض لطلب الدواء)
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'patient_profile')