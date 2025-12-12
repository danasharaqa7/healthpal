from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import HealthGuide, HealthAlert, Webinar
from django.utils import timezone

class EducationTests(APITestCase):
    
    def setUp(self):
        """
        تجهيز بيانات وهمية قبل كل اختبار
        """
        # 1. إنشاء دليل صحي (Guide)
        self.guide1 = HealthGuide.objects.create(
            title="دليل التغذية",
            content="محتوى عن التغذية السليمة...",
            category="NUTRITION",
            is_visual=False
        )
        self.guide2 = HealthGuide.objects.create(
            title="الإسعافات الأولية",
            content="كيف تتصرف في الطوارئ...",
            category="FIRST_AID",
            is_visual=True
        )

        # 2. إنشاء تنبيهات صحية (Alerts)
        # واحد نشط وواحد غير نشط عشان نفحص الفلتر
        self.active_alert = HealthAlert.objects.create(
            title="تنبيه كورونا",
            message="ارتفاع الحالات...",
            severity="HIGH",
            is_active=True
        )
        self.inactive_alert = HealthAlert.objects.create(
            title="تنبيه قديم",
            message="انتهت الموجة",
            severity="LOW",
            is_active=False
        )

        # 3. إنشاء ندوة (Webinar)
        self.webinar = Webinar.objects.create(
            title="الصحة النفسية في الحروب",
            description="نقاش مفتوح...",
            speaker="د. أحمد",
            date_time=timezone.now(),
            meeting_link="http://zoom.us/j/123456"
        )

        # الروابط (URLs)
        self.guides_url = reverse('health-guides')   # /api/v1/education/guides/
        self.alerts_url = reverse('health-alerts')   # /api/v1/education/alerts/
        self.webinars_url = reverse('webinars')      # /api/v1/education/webinars/

    def test_list_health_guides(self):
        """
        فحص 1: هل يتم عرض الأدلة الصحية للجميع؟
        """
        response = self.client.get(self.guides_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # لازم يرجع 2

    def test_search_health_guides(self):
        """
        فحص 2: هل البحث (SearchFilter) يعمل؟
        """
        # نبحث عن كلمة "تغذية"
        response = self.client.get(self.guides_url, {'search': 'التغذية'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "دليل التغذية")

    def test_list_only_active_alerts(self):
        """
        فحص 3: هل يعرض النظام التنبيهات النشطة فقط؟
        """
        response = self.client.get(self.alerts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # لازم يرجع 1 بس (لأنه الثاني is_active=False)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "تنبيه كورونا")

    def test_list_webinars(self):
        """
        فحص 4: هل يتم عرض الندوات؟
        """
        response = self.client.get(self.webinars_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['speaker'], "د. أحمد")
