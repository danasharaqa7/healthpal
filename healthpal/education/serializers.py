from rest_framework import serializers
from .models import HealthGuide, HealthAlert, Webinar

class HealthGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthGuide
        fields = ['id', 'title', 'content', 'category', 'is_visual', 'video_url', 'created_at']

class HealthAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthAlert
        fields = ['id', 'title', 'message', 'severity', 'location', 'is_active', 'created_at']

class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = ['id', 'title', 'description', 'speaker', 'date_time', 'meeting_link', 'created_at']