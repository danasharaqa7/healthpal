from django.urls import path
from . import views

urlpatterns = [
    # GET /api/v1/education/guides/
    path('guides/', views.HealthGuideListView.as_view(), name='health-guides'),

    # GET /api/v1/education/alerts/
    path('alerts/', views.HealthAlertListView.as_view(), name='health-alerts'),

    # GET /api/v1/education/webinars/
    path('webinars/', views.WebinarListView.as_view(), name='webinars'),
]