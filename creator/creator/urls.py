"""creator URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from member.views import kakao_login,kakao_callback,kakao_join
urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/',include('allauth.urls')),
    path('account/login/kakao/',kakao_login,name='kakao_login'),
    path('account/login/kakao/callback/',kakao_callback,name='kakao_callback'),
  	path('account/join/kakao/',kakao_join,name='kakao_join'),
    # path('account/registration/',include('rest_auth.registration.urls')),
    # path('account/',include('rest_auth_urls')),
    # url(r'account/registration/confirm-email/(?P<key>.+)/$',confirm_email,name="confirm_email"),
    # path('',include('django.contrib,auth,urls')),
    # Oauth urls
]

