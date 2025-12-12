from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User, Role, UserRole, PatientProfile
from .models import SponsorshipCase

class SponsorshipTests(APITestCase):
    
    def setUp(self):
        # 1. تجهيز الأدوار
        self.patient_role = Role.objects.create(name='PATIENT')
        self.donor_role = Role.objects.create(name='DONOR')

        # 2. مريض (صاحب الحالة)
        self.patient = User.objects.create_user(email='patient@test.com', password='123')
        UserRole.objects.create(user=self.patient, role=self.patient_role)
        self.profile = PatientProfile.objects.create(user=self.patient)

        # 3. متبرع
        self.donor = User.objects.create_user(email='donor@test.com', password='123')
        UserRole.objects.create(user=self.donor, role=self.donor_role)

        # 4. حالة كفالة
        self.case = SponsorshipCase.objects.create(
            patient=self.profile,
            title="عملية",
            treatment_type="SURGERY",
            donation_goal=1000,
            is_verified=True
        )

    def test_donation_updates_amount(self):
        """
        فحص: هل التبرع يزيد الرصيد فعلاً؟
        """
        self.client.force_authenticate(user=self.donor)
        
        # نتبرع بـ 100
        url = reverse('donate-to-case', kwargs={'case_id': self.case.id})
        data = {'amount': 100}
        
        response = self.client.post(url, data)
        
        # التأكد من النجاح
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # التأكد إن الرصيد صار 100
        self.case.refresh_from_db()
        self.assertEqual(self.case.current_donated_amount, 100)
