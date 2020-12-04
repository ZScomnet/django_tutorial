from django.shortcuts import render,HttpResponse,redirect
from django.http import Http404
from django.template import loader
from .models import Member
from .forms import Postform,Loginform

# Create your views here.
def join(request):
	return render(request,'Join\\Signin.html')

def join_member(request):
	if request.method == 'POST':
		form = Postform(request.POST)
		if form.is_valid():
			form.save()
			return render(request,"Join_check\\SignCheck.html",{"form":form})
		else:
			return HttpResponse(form)
	else:
		form = Postform()
		raise Http404

def login(request):
	return render(request,"login\\Login.html")

def login_check(request):
	if request.method == 'POST':
		member = Member.objects.all()
		ID = request.POST.get('ID','')
		Password = request.POST.get('Password','')
		for check in member:
			if check.ID == ID and check.Password == Password:
				request.session['username'] = ID
				return redirect('/')
		return render(request,"login\\Return_Rejection.html")
	else:
		form = Loginform()
		return HttpResponse("Only POST")

def logout(request):
	if request.session['username'] != None:
		del request.session['username']
		return redirect('/')
	else:
		return HttpResponse("No Log")