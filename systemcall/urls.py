"""systemcall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken.views import obtain_auth_token

from apps.registercall.views import RegisterCallViewSet
from apps.phonebill.views import PhoneBillViewSet
from apps.phonebill.views import RegisterViewSet

schema_view = get_swagger_view(title='System Call')

router = routers.DefaultRouter()
router.register(r'registercall', RegisterCallViewSet, base_name='RegisterCall')
router.register(r'phonebill', PhoneBillViewSet, base_name='PhoneBill')
router.register(r'registers', RegisterViewSet, base_name='Registers')

urlpatterns = [
    url(r'^$', schema_view),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token)
]
