from django.urls import path
from . import views



urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('delete_bmi/<int:bmi_id>/', views.delete_bmi, name='delete_bmi'),
    path('consultant/dashboard/', views.consultant_dashboard, name='consultant_dashboard'),
    path('consultant/assign/<int:student_id>/', views.assign_program, name='assign_program'),
    path('consultant/profile/', views.consultant_profile, name='consultant_profile'),
    path('consultant/manage/', views.manage_students, name='manage_students'),
    path('logout/', views.logout_view, name='logout'),
]
