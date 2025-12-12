# healthpal/users/models.py

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

class UserManager(BaseUserManager):
    """مدير مخصص لنموذج المستخدم حيث البريد الإلكتروني هو المعرف الفريد."""

    def create_user(self, email, password=None, **extra_fields):
        """إنشاء وحفظ مستخدم جديد مع الإيميل والباسورد."""
        if not email:
            raise ValueError('البريد الإلكتروني هو حقل إجباري (The email must be set)')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """إنشاء وحفظ مستخدم خارق (Superuser)."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    """نموذج المستخدم الأساسي في النظام."""
    
    email = models.EmailField(unique=True) 
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email




class Role(models.Model):
    """يخزن الصلاحيات المتاحة في النظام (e.g., PATIENT, DOCTOR)."""
    name = models.CharField(max_length=100, unique=True) # 'PATIENT', 'DOCTOR', 'DONOR'

    def __str__(self):
        return self.name

class UserRole(models.Model):
    """يربط المستخدمين بالصلاحيات (Many-to-Many)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_users')

    class Meta:
        unique_together = ('user', 'role') # نضمن عدم تكرار الصلاحية لنفس المستخدم

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"



class PatientProfile(models.Model):
    """يخزن المعلومات الإضافية الخاصة بالمرضى."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient_profile')
    medical_history = models.TextField(blank=True, null=True) # رح نشفره لاحقاً
    consent_given = models.BooleanField(default=False) # هل وافق على عرض حالته؟
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Patient Profile: {self.user.email}"


class Language(models.Model):
    """يخزن اللغات المتاحة للبحث."""
    name = models.CharField(max_length=100, unique=True) # e.g., "Arabic"
    code = models.CharField(max_length=10, unique=True) # e.g., "ar"

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    """يخزن المعلومات الإضافية الخاصة بالأطباء."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor_profile')
    specialty = models.CharField(max_length=255) # e.g., 'pediatrics'
    is_international = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False) # الـ Admin بعدلها
    
    # علاقة Many-to-Many الجديدة (v2.0) مع اللغات
    languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return f"Doctor Profile: {self.user.email}"