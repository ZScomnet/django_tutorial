from django.shortcuts import render,HttpResponse,redirect
from allauth.socialaccount.models import SocialApp
from allauth.account.models import EmailAddress
import urllib
import requests
import base64
import json
from .models import User
from django.views.generic import View
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.models import update_last_login
from django.contrib.auth import logout

class SignInView(View): # New_member View
	def get(self,request):
		return HttpResponse("Invalid access")
	def post(self,request):
		if User.objects.filter(ID=request.POST['username']):
			return HttpResponse("Exist ID already")
		else:
			new_member = User.objects.get(id=request.POST['id'])
			new_member.username = request.POST['username']
			new_member.ID = request.POST['ID']
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

class ChangeUserPasswordView(View):
	def get(self,request):
		return HttpResponse("Invalid access")
	def post(self,request):
		password = make_password(request.POST['password1'])
		change_member = User.objects.get(id=request.POST['id'])
		if check_password(request.POST['password2'],password) == False:
			return HttpResponse("Check Password")
		change_member.password = password
		change_member.save()
		return HttpResponse("Change password Complete!")

class CommunityLoginView(View): # LogincheckView
	def get(self, request):
		return HttpResponse("Invalid access")
	def post(self, request):
		try:
			member = User.objects.get(ID=request.POST['ID'])
			if check_password(request.POST['password'],member.password):
				update_last_login(None,member)
				request.session['username'] = member.username
				return redirect("/main/")
			else:
				return HttpResponse("Check your ID or password")
		except:
			return HttpResponse("Check your ID or password")

class CommunityLogoutView(View): # LogoutView
	def get(self,request):
		request.session.pop('username')
		return redirect("/main/")

class CommunitySelectionView(View): # Select social for finding user data
	host_url = 'http://localhost:8000'
	def get(self,request,social):
		request.session['find'] = True
		if social == "kakao":
			return redirect(self.host_url+"/account/login/"+social+"/")
		elif social == "google":
			return redirect(self.host_url+"/account/login/"+social+"/")

class SocialLoginView(View):
	def get(self, request, social):
		if social == "kakao":
			kakao_app = SocialApp.objects.get(provider="kakao")
			app_key = kakao_app.client_id
			return redirect("https://kauth.kakao.com/oauth/authorize?client_id="+app_key+"&redirect_uri=http://localhost:8000/account/login/kakao/callback/&response_type=code")

		elif social == "google":
			google_app = SocialApp.objects.get(provider="google")
			app_key = google_app.client_id
			return redirect("https://accounts.google.com/o/oauth2/auth?client_id="+app_key+"&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccount%2Flogin%2Fgoogle%2Fcallback%2F&scope=email%20profile&response_type=code&state=xUF6TP4C8S9y")

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
			if User.objects.filter(email=email).filter(account_info="kakao") and request.session['find']:
				# Find ID or Password
				send_id_row = User.objects.get(email=email)
				send_id = send_id_row.id
				request.session.pop('find')
				return render(request,"UserFindForm.html",{'ID':send_id_row.ID,'id':send_id})
			else: # Wrong information
				request.session.pop('find')
				return HttpResponse("Non-existent data")
		except KeyError: # New member Error
			if User.objects.filter(email=email).filter(account_info="kakao"):
				return HttpResponse("Exist member already")
			else:
				new_member = User(account_info="kakao",email=email)
				new_member.save()
				# Create new model for new member
				send_id_row = User.objects.get(email=email)
				send_id = send_id_row.id
				return render(request,"SignInForm.html",{'id' : send_id,})
		except:
			return HttpResponse("Invalid access")
		return HttpResponse("Invalid access")

class GoogleCallbackView(View):
	host_url = "http://localhost:8000"
	access_token_request_uri = 'https://oauth2.googleapis.com/token?'
	def get(self, request):
		code = request.GET['code']
		try:
			if request.session['find']:
				user_find = True
		except KeyError:
			user_find = False
		google_app = SocialApp.objects.get(provider="google")
		client_id = google_app.client_id
		client_secret = google_app.secret
		redirect_uri = self.host_url + '/account/login/google/callback/'
		self.access_token_request_uri += 'code=' + code + '&client_id=' + client_id + '&client_secret=' + client_secret + '&redirect_uri=' + redirect_uri + '&grant_type=authorization_code'	
		access_token_request = requests.post(self.access_token_request_uri)
		# Request access_token with id_token
		token_set = access_token_request.json() # 
		id_token_set = token_set.get("id_token").split('.')
		if len(id_token_set) != 3: # Invalid token
			return HttpResponse("Invalid data")

		b64_id_token = id_token_set[1]
		b64_id_token = b64_id_token + '=' * (4-len(b64_id_token)%4)
		id_token = base64.b64decode(b64_id_token) # User profile in token
		# Decode id_token in google request

		profile = json.loads(id_token)
		email = profile['email']
		logout(request) # google logout
		if User.objects.filter(email=email).filter(account_info="google") and user_find:
			# Find User ID or password
			send_id_row = User.objects.get(email=email)
			send_id = send_id_row.id
			return render(request,"UserFindForm.html",{'ID':send_id_row.ID,'id':send_id})
		elif user_find:
			return HttpResponse("Non-existent data")
		elif User.objects.filter(email=email).filter(account_info="google").filter(ID=""):
			# Error : Dummy data after to obtain account token
			send_id_row = User.objects.get(email=email)
			send_id = send_id_row.id
			return render(request,"SignInForm.html",{'id':send_id,})
		elif User.objects.filter(email=email).filter(account_info="google"):
			return HttpResponse("Exist member already")
		else:
			new_member = User(account_info="google",email=email)
			new_member.save()
			# Create new model for new member
			send_id_row = User.objects.get(email=email)
			send_id = send_id_row.id
			return render(request,"SignInForm.html",{'id':send_id,})
		# Create new model for new member	