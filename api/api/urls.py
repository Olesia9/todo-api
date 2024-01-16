"""api URL Configuration

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
from django.contrib import admin
from django.urls import path
from core import views

# Определяем точки входа
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_index, name='api_index'),
    path('all/', views.api_all_tasks, name='api_all_tasks'),
    path('new/', views.api_new_task, name='api_new_task'),
    path('update/', views.api_update_task, name='api_update_task'),
    path('delete/', views.api_delete_task, name='api_delete_task'),
    path('signin/', views.api_signin, name='api_signin'),
    path('register/', views.api_signup, name='api_signup')
]
