# healthpal/consultations/permissions.py

from rest_framework import permissions

class IsPatientUser(permissions.BasePermission):
    """
    صلاحية مخصصة (Custom Permission) للتأكد أن المستخدم هو "مريض".
    (رح نستخدمها عشان نسمح "بس" للمرضى يحجزوا مواعيد).
    """
    message = 'فقط المستخدمين بصلاحية "مريض" (Patient) يمكنهم تنفيذ هذا الإجراء.'

    def has_permission(self, request, view):
        # 1. هل هو مسجل دخول؟
        if not request.user or not request.user.is_authenticated:
            return False
        # 2. هل عنده "ملف مريض"؟
        return hasattr(request.user, 'patient_profile')

class IsDoctorUser(permissions.BasePermission):
    """
    صلاحية مخصصة (Custom Permission) للتأكد أن المستخدم هو "دكتور".
    (رح نستخدمها عشان نسمح "بس" للدكاترة يضيفوا مواعيد).
    """
    message = 'فقط المستخدمين بصلاحية "دكتور" (Doctor) يمكنهم تنفيذ هذا الإجراء.'

    def has_permission(self, request, view):
        # 1. هل هو مسجل دخول؟
        if not request.user or not request.user.is_authenticated:
            return False
        # 2. هل عنده "ملف دكتور"؟
        return hasattr(request.user, 'doctor_profile')