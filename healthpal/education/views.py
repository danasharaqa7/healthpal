from rest_framework import generics, permissions, filters
from .models import HealthGuide, HealthAlert, Webinar
from .serializers import HealthGuideSerializer, HealthAlertSerializer, WebinarSerializer

# 1. عرض الأدلة الصحية
class HealthGuideListView(generics.ListAPIView):
    """
    GET: عرض قائمة الأدلة الصحية (مع إمكانية البحث حسب الفئة).
    """
    queryset = HealthGuide.objects.all()
    serializer_class = HealthGuideSerializer
    permission_classes = [permissions.AllowAny] # متاح للجميع (Public)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category']

# 2. عرض الإنذارات الصحية
class HealthAlertListView(generics.ListAPIView):
    """
    GET: عرض الإنذارات الصحية النشطة فقط.
    """
    # بنجيب بس الإنذارات اللي "is_active=True"
    queryset = HealthAlert.objects.filter(is_active=True)
    serializer_class = HealthAlertSerializer
    permission_classes = [permissions.AllowAny]

# 3. عرض الندوات
class WebinarListView(generics.ListAPIView):
    """
    GET: عرض الندوات القادمة.
    """
    queryset = Webinar.objects.all().order_by('date_time')
    serializer_class = WebinarSerializer
    permission_classes = [permissions.AllowAny]