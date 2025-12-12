from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, Role, UserRole, PatientProfile, DoctorProfile
from .models import DoctorAvailabilitySlot, Consultation
from django.utils import timezone
import datetime

class ConsultationTests(APITestCase):
    
    def setUp(self):
        # 1. تجهيز الأدوار
        self.patient_role = Role.objects.create(name='PATIENT')
        self.doctor_role = Role.objects.create(name='DOCTOR')

        # 2. تجهيز مريض (Dana)
        self.patient_user = User.objects.create_user(email='patient@test.com', password='password123')
        UserRole.objects.create(user=self.patient_user, role=self.patient_role)
        PatientProfile.objects.create(user=self.patient_user)

        # 3. تجهيز دكتور (Ahmad)
        self.doctor_user = User.objects.create_user(email='doctor@test.com', password='password123')
        UserRole.objects.create(user=self.doctor_user, role=self.doctor_role)
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor_user, specialty='General')

        # 4. تجهيز موعد متاح (Slot)
        start_time = timezone.now() + datetime.timedelta(days=1)
        end_time = start_time + datetime.timedelta(minutes=30)
        self.slot = DoctorAvailabilitySlot.objects.create(
            doctor=self.doctor_profile,
            start_time=start_time,
            end_time=end_time,
            is_booked=False
        )

        self.url = reverse('consultation-list-create') # /api/v1/consultations/

    def test_book_consultation_success(self):
        """
        فحص 1: حجز موعد متاح بنجاح.
        """
        self.client.force_authenticate(user=self.patient_user)
        data = {'availability_slot_id': self.slot.id}
        
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.slot.refresh_from_db()
        self.assertTrue(self.slot.is_booked) # لازم الموعد يصير محجوز

    def test_book_booked_slot_fail(self):
        """
        فحص 2: محاولة حجز موعد محجوز مسبقاً (يجب أن تفشل).
        """
        # أولاً: نحجز الموعد يدوياً
        self.slot.is_booked = True
        self.slot.save()

        # ثانياً: نحاول نحجزه مرة ثانية
        self.client.force_authenticate(user=self.patient_user)
        data = {'availability_slot_id': self.slot.id}
        
        response = self.client.post(self.url, data)
        
        # لازم يعطي خطأ 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)