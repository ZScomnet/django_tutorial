from django.shortcuts import render,HttpResponse,redirect
from allauth.socialaccount.models import SocialApp,SocialAccount
import urllib
import requests
from .models import User
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.models import update_last_login

def kakao_login(request):
	kakao_app = SocialApp.objects.get(provider="kakao")
	app_key = kakao_app.client_id
	return redirect("https://kauth.kakao.com/oauth/authorize?client_id="+app_key+"&redirect_uri=http://localhost:8000/account/login/kakao/callback/&response_type=code")

def kakao_logout(request):
	kakao_app = SocialApp.objects.get(provider="kakao")
	client_id = kakao_app.client_id
	redirect_uri = 'http://localhost:8000/account/logout/kakao/'

def kakao_join(request):
	# After authorize, add new member data in member_User
	if request.method == 'POST':
		if User.objects.filter(ID=request.POST['username']):
			return HttpResponse("Exist ID already")
			# exist ID
		else:
			new_member = User.objects.get(id=request.POST['id'])
			new_member.name = request.POST['name']
			new_member.ID = request.POST['username']
			new_member.password = make_password(request.POST['password1'])
			new_member.tel = request.POST['tel']
			kakao_token_delete = requests.get(
				"https://kapi.kakao.com/",
				headers={"Authorization" : f"Bearer {new_member.access_token}"},
			) # Kakao logout
			new_member.access_token = ""
			new_member.save()
			# Save new member data
			return HttpResponse("Join Complete")
	else:
		return HttpResponse("Invalid access")

def kakao_callback(request):
	code = request.GET['code']
	kakao_app = SocialApp.objects.get(provider="kakao")
	client_id = kakao_app.client_id
	redirect_uri = 'http://localhost:8000/account/login/kakao/callback/'
	access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
	access_token_request_uri += "client_id=" + client_id
	access_token_request_uri += "&redirect_uri=" + redirect_uri
	access_token_request_uri += "&code=" + code

	access_token_request = requests.get(access_token_request_uri)
	token_set = access_token_request.json()
	error = token_set.get("error",None)
	# Request access token
	if error is not None: # Inalid token
		return HttpResponse("Invalid code")

	access_token = token_set.get("access_token")
	profile_request = requests.get(
			"https://kapi.kakao.com/v2/user/me",
			headers={"Authorization" : f"Bearer {access_token}"},
		)
	# Request profile information
	profile_request_json = profile_request.json()
	profile = profile_request_json['kakao_account']
	profile_email = profile['email']
	new_member = User(email=profile_email,account_info="kakao",access_token=access_token)
	new_member.save()
	# Create new model for new member

	send_id_column = User.objects.get(email=profile_email)
	send_id = send_id_column.id
	return render(request,"send.html",{'id' : send_id,})
	# Input other data(ID,password,Tel etc..)