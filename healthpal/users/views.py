# healthpal/users/views.py

from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer, UserDisplaySerializer
from .models import User

class UserRegistrationView(generics.CreateAPIView):
    """
    View لتسجيل مستخدم جديد (Endpoint: POST /api/v1/auth/register).
    (مطابق لتصميم v2.0 ملف 12، [cite: 559])
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # أي حدا بقدر يسجل


class UserMeView(generics.RetrieveUpdateAPIView):
    """
    View لجلب (GET) أو تعديل (PATCH) بيانات المستخدم الحالي.
    (Endpoint: GET/PATCH /api/v1/users/me).
    (مطابق لتصميم v2.0 ملف 12، [cite: 567, 569])
    """
    serializer_class = UserDisplaySerializer # بنستخدم هاد للـ GET
    permission_classes = [permissions.IsAuthenticated] # لازم يكون مسجل دخول

    def get_object(self):
        """
        هاي الـ function بترجع "المستخدم الحالي" (اللي باعت التوكن)
        """
        return self.request.user
    
    # (ملاحظة: رح نحتاج نعمل Serializer خاص للـ Update (PATCH) لاحقاً
    # بس حالياً هاد بكفي للـ GET)