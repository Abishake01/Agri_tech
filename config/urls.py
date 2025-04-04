"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from agriai import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('crop-recommendation/', views.crop_recommendation, name='crop_recommendation'),
    path('water-management/', views.water_management, name='water_management'),
    path('voice-assistant/', views.voice_assistant, name='voice_assistant'),
    path('voice-assistant-api/', views.voice_assistant_api, name='voice_assistant_api'),
    path('voice-query/', views.voice_query_api, name='voice_query_api'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)