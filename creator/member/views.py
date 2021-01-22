from django.shortcuts import render,HttpResponse,redirect
from allauth.socialaccount.models import SocialApp,SocialAccount
import urllib
import requests
from .models import User
from django.views.generic import View
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.models import update_last_login

class SignInView(View):
	def get(self,request):
		return HttpResponse("Invalid access")
	def post(self,request):
		if User.objects.filter(ID=request.POST['username']):
			return HttpResponse("Exist ID already")
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

class CommunityLoginView(View):
	def get(self, request):
		return HttpResponse("Invalid access")

	def post(self, request):
		try:
			member = User.objects.get(ID=request.POST['ID'])
			if check_password(request.POST['password'],member.password):
				update_last_login(None,member)
				request.session['username'] = member.name
				return redirect("/main/")
			else:
				return HttpResponse("Check your ID or Password")
		except:
			return HttpResponse("Check your ID or Password")

class CommunityLogoutView(View):
	def get(self,request):
		request.session.pop('user')
		return redirect("/main/")

class SocialLoginView(View):
	def get(self, request, social):
		if social == "kakao":
			kakao_app = SocialApp.objects.get(provider="kakao")
			app_key = kakao_app.client_id
			return redirect("https://kauth.kakao.com/oauth/authorize?client_id="+app_key+"&redirect_uri=http://localhost:8000/account/login/kakao/callback/&response_type=code")

		elif social == "google":
			google_app = SocialApp.objects.get(provider="google")
			app_key = google_app.client_id
			return redirect("https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?client_id="+app_key+"&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccount%2Fgoogle%2Flogin%2Fcallback%2F&scope=email%20profile&response_type=code&state=xUF6TP4C8S9y&flowName=GeneralOAuthFlow")

# class GoogleCallbackView(View):



class KakaoCallbackView(View):
	host_url = 'http://localhost:8000'
	access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"

	def get(self, request):
		code = request.GET['code']
		kakao_app = SocialApp.objects.get(provider="kakao")
		client_id = kakao_app.client_id
		redirect_uri = self.host_url + '/account/login/kakao/callback/'
		self.access_token_request_uri += "client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&code=" + code
		access_token_request = requests.get(self.access_token_request_uri)
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
		try:
			kakao_token_delete = requests.get(
					"https://kapi.kakao.com/v1/user/unlink",
					headers={"Authorization" : f"Bearer {access_token}"},
			) # Kakao logout
			email = profile['email']
			new_member = User(account_info="kakao",email=email)
			new_member.save()
			# Create new model for new member

			send_id_column = User.objects.get(email=email)
			send_id = send_id_column.id
			return render(request,"SignInForm.html",{'id' : send_id,})
		except:
			return HttpResponse("Check to provide Email")
		# Input other data(ID,password,Tel etc..)

# class GoogleCallbackView(View):
# 	def get(self, request):