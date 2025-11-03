# healthpal/users/serializers.py

from rest_framework import serializers
from .models import User, Role, UserRole, PatientProfile, DoctorProfile, Language


class PatientProfileSerializer(serializers.ModelSerializer):
    """
    Serializer لملف المريض.
    (حسب تصميم v2.0 ملف 13، [cite: 101])
    """
    class Meta:
        model = PatientProfile
        fields = ['location', 'medical_history', 'consent_given']


class DoctorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer لملف الطبيب.
    (حسب تصميم v2.0 ملف 13، [cite: 106])
    """
    language_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = DoctorProfile
        fields = ['specialty', 'is_international', 'language_ids']
    
    def create(self, validated_data):
        language_ids = validated_data.pop('language_ids', [])
        profile = DoctorProfile.objects.create(**validated_data)
        if language_ids:
            languages = Language.objects.filter(id__in=language_ids)
            profile.languages.set(languages)
        return profile


# --- Serializer تسجيل مستخدم جديد. 

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer لتسجيل مستخدم جديد.
    (حسب تصميم v2.0 ملف 13، [cite: 92])
    """
    # بنخليه للكتابة فقط (write_only) عشان ما نرجعه بالـ response
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    # (v2.0) بنستقبل قائمة "أرقام" (IDs) للصلاحيات
    roles = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )

    # (v2.0) بنستقبل بيانات الـ profiles (اختياري)
    patient_profile = PatientProfileSerializer(required=False, write_only=True)
    doctor_profile = DoctorProfileSerializer(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 
            'password', 
            'first_name', 
            'last_name', 
            'roles', 
            'patient_profile', 
            'doctor_profile'
        ]

    def create(self, validated_data):
        """
        إنشاء المستخدم، تشفير كلمة المرور، وربط الصلاحيات والملفات.
        """
        # 1. بنفصل البيانات عن بعض
        roles_data = validated_data.pop('roles')
        patient_data = validated_data.pop('patient_profile', None)
        doctor_data = validated_data.pop('doctor_profile', None)
        
        # 2. بننشئ المستخدم (User)
        # (بنستخدم create_user عشان نضمن تشفير الباسورد)
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        # 3. بنربط الصلاحيات (Roles)
        roles = Role.objects.filter(id__in=roles_data)
        for role in roles:
            UserRole.objects.create(user=user, role=role)

        # 4. بننشئ ملف المريض (PatientProfile) (إذا تم إرساله)
        if patient_data:
            PatientProfile.objects.create(user=user, **patient_data)

        # 5. بننشئ ملف الطبيب (DoctorProfile) (إذا تم إرساله)
        if doctor_data:
            # بنستخدم الـ create المخصص تاع الدكتور عشان يربط اللغات
            DoctorProfileSerializer().create(validated_data={'user': user, **doctor_data})

        return user


# --- Serializer عرض بيانات المستخدم (لـ users/me) ---

class UserDisplaySerializer(serializers.ModelSerializer):
    """
    Serializer لعرض بيانات المستخدم (ملفي الشخصي).
    (حسب تصميم v2.0 ملف 13، [cite: 114])
    """
    # بنجيب الصلاحيات وبنحولها لـ "قائمة أسماء" (strings)
    roles = serializers.SerializerMethodField()
    
    # بنعرض الـ profiles (للقراءة فقط)
    patient_profile = PatientProfileSerializer(read_only=True)
    doctor_profile = DoctorProfileSerializer(read_only=True) # (ملاحظة: رح نحتاج نعدله ليعرض اللغات كأسماء)

    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'roles', 
            'patient_profile', 
            'doctor_profile'
        ]
        read_only_fields = fields 

    def get_roles(self, obj):
        return [user_role.role.name for user_role in obj.user_roles.all()]