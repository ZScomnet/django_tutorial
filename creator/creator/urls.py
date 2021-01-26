from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url,re_path

from member.views import (SignInView,GoogleCallbackView,KakaoCallbackView,SocialLoginView,
	CommunityLoginView,CommunityLogoutView)
from main.views import MainFormView,LoginFormView
urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/',include('allauth.urls')),
    path('account/login/<social>/',SocialLoginView.as_view(),name='SocialLogin'),
    path('account/login/kakao/callback/',KakaoCallbackView.as_view(),name='KakaoCallback'),
    path('account/login/google/callback/',GoogleCallbackView.as_view(),name='GoogleCallback'),
  	path('account/join/',SignInView.as_view(),name='SignIn'),
  	path('account/member/login/',CommunityLoginView.as_view(),name='CommunityLogin'),
    # Oauth urls

    path('main/',MainFormView.as_view(),name="MainForm"),
    path('main/login/',LoginFormView.as_view(),name="LoginForm"),
    path('main/logout/',CommunityLogoutView.as_view(),name='CommunityLogout')
    # Community Forms urls
]

