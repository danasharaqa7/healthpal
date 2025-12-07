from rest_framework import generics, permissions, filters
from .models import MedicalItem, InventoryItem, ItemRequest
from .serializers import (
    MedicalItemSerializer, 
    InventoryItemSerializer, 
    ItemRequestSerializer,
    ItemRequestFulfillSerializer
)
from .permissions import IsDistributorUser, IsNGOStaffUser, IsPatientUser

# 1. قائمة الأدوية والمعدات (للكل)
class MedicalItemListView(generics.ListAPIView):
    queryset = MedicalItem.objects.all()
    serializer_class = MedicalItemSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

# 2. إدارة المخزون (عرض للكل، إضافة للموزع)
class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.filter(quantity__gt=0) # بس اللي فيه كمية
    serializer_class = InventoryItemSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsDistributorUser()] # بس الموزع بضيف
        return [permissions.AllowAny()] # الكل بشوف المتوفر

# 3. طلبات المرضى (إنشاء للمريض، عرض للـ NGO)
class ItemRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = ItemRequestSerializer

    def get_queryset(self):
        user = self.request.user
        # الـ NGO بتشوف كل الطلبات المعلقة
        if user.user_roles.filter(role__name='NGO_STAFF').exists():
            return ItemRequest.objects.filter(status='PENDING')
        # المريض بشوف طلباته هو بس
        elif hasattr(user, 'patient_profile'):
            return ItemRequest.objects.filter(patient=user.patient_profile)
        return ItemRequest.objects.none()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsPatientUser()]
        return [permissions.IsAuthenticated()]

# 4. تلبية الطلب (للـ NGO فقط)
class FulfillRequestView(generics.UpdateAPIView):
    queryset = ItemRequest.objects.all()
    serializer_class = ItemRequestFulfillSerializer
    permission_classes = [IsNGOStaffUser]
    lookup_field = 'id'