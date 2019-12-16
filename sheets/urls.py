"""sheets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings

from practices.views import show_list, my_logout, update_sheet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', show_list, name='list'),
    path('update_sheet/<int:id>/', update_sheet, name='super_sheet'),
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^logout/$', my_logout, name='super_logout'),
]
