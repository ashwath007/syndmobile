"""syndMobile URL Configuration

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
from django.urls import path

from verification.views import read_email_from_gmail, create_uudi_hash, is_registered

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verify/', read_email_from_gmail),
    path('uuid/', create_uudi_hash),
    path('isRegistered/', is_registered),
]
