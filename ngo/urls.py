from django.urls import path
from . import views

urlpatterns = [
    # GET /api/v1/ngo/list/
    path('list/', views.NGOListView.as_view(), name='ngo-list'),

    # GET /api/v1/ngo/missions/
    path('missions/', views.MedicalMissionListView.as_view(), name='mission-list'),
]