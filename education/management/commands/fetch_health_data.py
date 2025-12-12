import requests
from django.core.management.base import BaseCommand
from education.models import HealthAlert

class Command(BaseCommand):
    help = 'Fetches COVID-19 data for Palestine from an external API'

    def handle(self, *args, **kwargs):
        # رابط الـ API الخارجي (Disease.sh)
        url = "https://disease.sh/v3/covid-19/countries/palestine"
        
        self.stdout.write("Connecting to external API...")

        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # استخراج البيانات المهمة
                cases = data.get('cases')
                recovered = data.get('recovered')
                deaths = data.get('deaths')
                active = data.get('active')
                
                # تجهيز نص الإنذار
                alert_title = "تحديث إحصائيات كورونا - فلسطين"
                alert_message = (
                    f"أحدث البيانات من المصادر العالمية:\n"
                    f"- مجموع الحالات: {cases}\n"
                    f"- حالات الشفاء: {recovered}\n"
                    f"- الحالات النشطة: {active}\n"
                    f"- الوفيات: {deaths}\n"
                    f"يرجى توخي الحذر واتباع التعليمات الصحية."
                )
                
                # حفظ الإنذار في قاعدة البيانات عندنا
                HealthAlert.objects.create(
                    title=alert_title,
                    message=alert_message,
                    severity='HIGH', # نعتبره مهم
                    is_active=True,
                    location="Palestine"
                )
                
                self.stdout.write(self.style.SUCCESS('Successfully fetched and created Health Alert!'))
            else:
                self.stdout.write(self.style.ERROR('Failed to fetch data from API'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))