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
from django.contrib.auth import views as auth_views

from member.views import SignInView,KakaoCallbackView,SocialLoginView,CommunityLoginView
from main.views import LoginFormView
urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/login/<social>/',SocialLoginView.as_view(),name='SocialLogin'),
    path('account/login/kakao/callback/',KakaoCallbackView.as_view(),name='KakaoCallback'),
  	path('account/join/',SignInView.as_view(),name='SignIn'),
  	path('account/member/login/',CommunityLoginView.as_view(),name='CommunityLogin'),
    # path('account/registration/',include('rest_auth.registration.urls')),
    # path('account/',include('rest_auth_urls')),
    # url(r'account/registration/confirm-email/(?P<key>.+)/$',confirm_email,name="confirm_email"),
    # path('',include('django.contrib,auth,urls')),
    # Oauth urls

    path('main/login/',LoginFormView.as_view(),name="LoginForm")
    # Community Forms urls
]

