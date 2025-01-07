from django.urls import path
from hospital_app import views

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('register/', views.patient_register, name='patient_register'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
]
