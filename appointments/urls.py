from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('teacher-list/', views.teacher_list, name='teacher_list'),
    path('teacher/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('book/<int:teacher_id>/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('register/', views.register, name='register'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-appointments/', views.manage_appointments, name='manage_appointments'),
    path('approve-appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
]