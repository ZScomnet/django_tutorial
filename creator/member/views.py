from django.shortcuts import render,HttpResponse,redirect
from allauth.socialaccount.models import SocialApp,SocialAccount
import urllib

def kakao_login(request):
	kakao_app = SocialApp.objects.get(provider="kakao")
	app_key = kakao_app.client_id
	return redirect("https://kauth.kakao.com/oauth/authorize?client_id="+"481e0840e20536662de4f736e7b0cf70"+"&redirect_uri=http://localhost:8000/account/login/kakao/callback/&response_type=code")

def kakao_callback(request):
	params = urllib.parse.urlencode(request.GET)
	return HttpResponse(params)