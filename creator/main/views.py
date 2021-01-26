from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from allauth.account.models import EmailAddress

class MainFormView(View):
	def get(self,request):
		return HttpResponse("Login")

class LoginFormView(View):
	def get(self,request):
		return render(request,"LoginForm.html")