from django.urls import path
from . import views

urlpatterns = [
    # 1. قائمة الأدوية التعريفية
    path('medical-items/', views.MedicalItemListView.as_view(), name='medical-items'),

    # 2. المخزون (المتوفر)
    path('items/', views.InventoryListCreateView.as_view(), name='inventory-list-create'),

    # 3. طلبات المرضى
    path('requests/', views.ItemRequestListCreateView.as_view(), name='request-list-create'),

    # 4. تلبية طلب (لـ NGO)
    path('requests/<int:id>/fulfill/', views.FulfillRequestView.as_view(), name='fulfill-request'),
]