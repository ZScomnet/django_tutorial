from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View

class MainFormView(View):
	def get(self,request):
		return HttpResponse("main")

class LoginFormView(View):
	def get(self,request):
		return render(request,"LoginForm.html")