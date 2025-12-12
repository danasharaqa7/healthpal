from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User, Role, UserRole, PatientProfile
from .models import MedicalItem, InventoryItem, ItemRequest

class InventoryTests(APITestCase):
    
    def setUp(self):
        # 1. تجهيز الأدوار
        self.distributor_role = Role.objects.create(name='DISTRIBUTOR')
        self.patient_role = Role.objects.create(name='PATIENT')
        self.ngo_role = Role.objects.create(name='NGO_STAFF')

        # 2. تجهيز المستخدمين
        # موزع
        self.distributor = User.objects.create_user(email='dist@test.com', password='123')
        UserRole.objects.create(user=self.distributor, role=self.distributor_role)
        
        # مريض
        self.patient = User.objects.create_user(email='patient@test.com', password='123')
        UserRole.objects.create(user=self.patient, role=self.patient_role)
        PatientProfile.objects.create(user=self.patient)

        # موظف NGO
        self.ngo_staff = User.objects.create_user(email='ngo@test.com', password='123')
        UserRole.objects.create(user=self.ngo_staff, role=self.ngo_role)

        # 3. تجهيز دواء في النظام
        self.item = MedicalItem.objects.create(name="Panadol", item_type="MEDICINE")

    def test_distributor_add_inventory(self):
        """
        فحص 1: هل يستطيع الموزع إضافة مخزون؟
        """
        self.client.force_authenticate(user=self.distributor)
        url = reverse('inventory-list-create') # /api/v1/inventory/items/
        data = {
            'item_id': self.item.id,
            'quantity': 50,
            'location': 'Ramallah'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_request_item(self):
        """
        فحص 2: هل يستطيع المريض طلب دواء؟
        """
        self.client.force_authenticate(user=self.patient)
        url = reverse('request-list-create') # /api/v1/inventory/requests/
        data = {
            'item_id': self.item.id,
            'quantity_needed': 2
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ItemRequest.objects.count(), 1)

    def test_ngo_fulfill_request(self):
        """
        فحص 3: هل تستطيع الـ NGO تلبية الطلب؟
        """
        # ننشئ طلب معلق أولاً
        request = ItemRequest.objects.create(
            patient=self.patient.patient_profile,
            item=self.item,
            quantity_needed=1,
            status='PENDING'
        )

        self.client.force_authenticate(user=self.ngo_staff)
        url = reverse('fulfill-request', kwargs={'id': request.id})
        data = {'status': 'FULFILLED'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # نتأكد إن الحالة تغيرت وإن الموظف تسجل اسمه
        request.refresh_from_db()
        self.assertEqual(request.status, 'FULFILLED')
        self.assertEqual(request.fulfilled_by, self.ngo_staff)
