"""
URL configuration for MVP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from Test.admin_views import load_branch_offices, load_locations, get_applicants

urlpatterns = [
    path('admin/load-branch-offices/', load_branch_offices, name='load_branch_offices'),
    path('admin/load-locations/', load_locations, name='load_locations'),
    path('admin/get_applicants/', get_applicants, name='get_applicants'),
    path('admin/', admin.site.urls),
    path('', admin.site.urls)
    ]
