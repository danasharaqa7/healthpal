from rest_framework import serializers
from .models import MedicalItem, InventoryItem, ItemRequest
from users.serializers import UserDisplaySerializer

class MedicalItemSerializer(serializers.ModelSerializer):
    """
    عرض تفاصيل الدواء/المعدة (للقراءة فقط).
    """
    class Meta:
        model = MedicalItem
        fields = ['id', 'name', 'item_type', 'description']


class InventoryItemSerializer(serializers.ModelSerializer):
    """
    عرض وإضافة المخزون (للموزعين).
    """
    item = MedicalItemSerializer(read_only=True)
    item_id = serializers.IntegerField(write_only=True)
    
    distributor = UserDisplaySerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'item', 'item_id', 'distributor', 'quantity', 'expiry_date', 'location', 'created_at']

    def create(self, validated_data):
        # بنربط العنصر بالموزع الحالي
        validated_data['distributor'] = self.context['request'].user
        return super().create(validated_data)


class ItemRequestSerializer(serializers.ModelSerializer):
    """
    للمريض: إنشاء طلب جديد.
    للـ NGO: عرض الطلبات.
    """
    item = MedicalItemSerializer(read_only=True)
    item_id = serializers.IntegerField(write_only=True)
    
    patient = UserDisplaySerializer(source='patient.user', read_only=True)
    fulfilled_by = UserDisplaySerializer(read_only=True)

    class Meta:
        model = ItemRequest
        fields = ['id', 'patient', 'item', 'item_id', 'quantity_needed', 'status', 'fulfilled_by', 'created_at']
        read_only_fields = ['status', 'fulfilled_by']

    def create(self, validated_data):
        # بنربط الطلب بالمريض الحالي
        validated_data['patient'] = self.context['request'].user.patient_profile
        return super().create(validated_data)


class ItemRequestFulfillSerializer(serializers.ModelSerializer):
    """
    خاص بالـ NGO لتغيير حالة الطلب (تلبية الطلب).
    """
    class Meta:
        model = ItemRequest
        fields = ['status']

    def update(self, instance, validated_data):
        # بنسجل مين موظف الـ NGO اللي لبى الطلب
        instance.status = validated_data.get('status', instance.status)
        instance.fulfilled_by = self.context['request'].user
        instance.save()
        return instance