"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from leaves import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home' ),
    path('login/', views.user_login, name='login' ),
    path('dashboard/supervisor', views.supervisor_view, name='supervisor_view' ),
    path('dashboard/employee', views.employee_dashboard, name='employee_view' ),
    path('leave-request', views.leave_request, name='leave-request' ),
    path('leave-request/approve/<int:id>/', views.approve_leave, name='approve' ),
    path('leave-request/reject/<int:id>/', views.reject_leave, name='reject' ),
    path('profile/update', views.profile, name='profile-update' ),

]
