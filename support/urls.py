from django.urls import path
from . import views

urlpatterns = [
    # عرض المجموعات
    path('groups/', views.SupportGroupListView.as_view(), name='support-groups'),

    # بدء جلسة دردشة
    path('chat/start/', views.StartAnonymousChatView.as_view(), name='start-chat'),

    # إرسال واستقبال الرسائل
    path('chat/<uuid:session_id>/messages/', views.ChatMessageListCreateView.as_view(), name='chat-messages'),
]