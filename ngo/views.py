from rest_framework import generics, permissions, filters
from .models import NGO, MedicalMission
from .serializers import NGOSerializer, MedicalMissionSerializer

# 1. قائمة المنظمات الموثقة
class NGOListView(generics.ListAPIView):
    """
    GET: عرض كل المنظمات الموثقة (Verified NGOs).
    """
    # بنجيب بس اللي عليهم صح (Verified)
    queryset = NGO.objects.filter(is_verified=True)
    serializer_class = NGOSerializer
    permission_classes = [permissions.AllowAny] # متاح للجميع
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

# 2. قائمة البعثات الطبية
class MedicalMissionListView(generics.ListAPIView):
    """
    GET: عرض البعثات الطبية القادمة (Surgical Missions Tracker).
    """
    queryset = MedicalMission.objects.all().order_by('start_date')
    serializer_class = MedicalMissionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'location', 'specialties_available']