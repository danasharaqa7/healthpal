from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Role, UserRole

class UserTests(APITestCase):
    
    def setUp(self):
        """
        تجهيز البيانات قبل كل فحص (هذه الدالة تعمل أوتوماتيكياً).
        """
        # 1. ننشئ الصلاحيات الأساسية في داتابيس الفحص
        self.patient_role = Role.objects.create(name='PATIENT')
        self.doctor_role = Role.objects.create(name='DOCTOR')

        # 2. ننشئ مستخدم تجريبي للفحص
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        # نعطيه صلاحية مريض
        UserRole.objects.create(user=self.user, role=self.patient_role)

        # 3. نحفظ الروابط (URLs) اللي بدنا نفحصها
        self.register_url = reverse('register') # /api/v1/auth/register/
        self.me_url = reverse('user-me')        # /api/v1/auth/me/

    def test_registration_success(self):
        """
        فحص 1: هل التسجيل يعمل بشكل صحيح؟
        """
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
            "roles": [self.patient_role.id] # بنبعت رقم الرول
        }
        response = self.client.post(self.register_url, data, format='json')
        
        # لازم النتيجة تكون 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # لازم الإيميل يكون موجود في الرد
        self.assertEqual(response.data['email'], "newuser@example.com")

    def test_registration_duplicate_email(self):
        """
        فحص 2: هل يمنع النظام تسجيل نفس الإيميل مرتين؟
        """
        data = {
            "email": "testuser@example.com", # هذا الإيميل موجود أصلاً (أنشأناه في setUp)
            "password": "anotherpassword",
            "first_name": "Another",
            "last_name": "User",
            "roles": [self.patient_role.id]
        }
        response = self.client.post(self.register_url, data, format='json')
        
        # لازم النتيجة تكون 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_me_authenticated(self):
        """
        فحص 3: هل يستطيع المستخدم المسجل رؤية بياناته؟
        """
        # بنعمل "تسجيل دخول وهمي" (Force Authenticate)
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.me_url)
        
        # لازم النتيجة تكون 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_me_unauthenticated(self):
        """
        فحص 4: هل يُمنع الغريب من رؤية البيانات؟
        """
        # ما عملنا login هون
        response = self.client.get(self.me_url)
        
        # لازم النتيجة تكون 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)