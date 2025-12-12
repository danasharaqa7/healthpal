from rest_framework import serializers
from .models import NGO, MedicalMission

class NGOSerializer(serializers.ModelSerializer):
    """
    عرض تفاصيل المنظمة.
    """
    class Meta:
        model = NGO
        fields = ['id', 'name', 'description', 'website', 'logo', 'is_verified']

class MedicalMissionSerializer(serializers.ModelSerializer):
    """
    عرض تفاصيل البعثة الطبية.
    """
    # بنعرض تفاصيل المنظمة المسؤولة عن البعثة
    ngo = NGOSerializer(read_only=True)

    class Meta:
        model = MedicalMission
        fields = [
            'id', 'title', 'ngo', 'mission_type', 'description', 
            'location', 'start_date', 'end_date', 'specialties_available'
        ]