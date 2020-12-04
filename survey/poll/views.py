from django.shortcuts import render,HttpResponse,redirect
from django.template import loader
from .models import Poll,Submit_Poll_Table
from .forms import Pollform

def poll_page(request):
	poll_db = Poll.objects.all()
	if request.session.get('username') != None:
		return render(request,"QuestionForm\\QuestionForm.html",{'poll_db':poll_db})
	else:
		return render(request,"LoginCheck\\LoginCheck.html")

def poll_detail_page(request):
	poll_db = Poll.objects.all()
	if request.session.get('username') != None:
		return render(request,"QuestionDetailForm\\QuestionDetailForm.html",{'poll_db':poll_db})
	else:
		return render(request,"LoginCheck\\LoginCheck.html")

def poll_page_admin(request):
	poll_db = Poll.objects.all()
	if request.session.get('username') == 'khanaxbio':
		return render(request,"QuestionForm_admin\\QuestionForm_admin.html",{'poll_db':poll_db})
	else:
		return render(request,"Wrong_Approach\\Wrong_Approach.html")	

def poll_detail_page_admin(request):
	poll_db = Poll.objects.all()
	if request.session.get('username') == 'khanaxbio':
		return render(request,"QuestionForm_admin\\QuestionForm_admin.html",{'poll_db':poll_db})
	else:
		return render(request,"Wrong_Approach\\Wrong_Approach.html")	
		
def question_entry_page(request):
	if request.session.get('username') == 'khanaxbio':
		return render(request,"QuestionEntryForm\\QuestionEntryForm.html")
	else:
		return render(request,"Wrong_Approach\\Wrong_Approach.html")

def question_entry(request): # Question Insert and Update
	if request.method == 'POST':
		poll_db = Poll.objects.all()
		form = Pollform(request.POST)
		if form.is_valid():
			try:
				if request.POST.get("id","") != None: # Question Update
					update_data_row = Poll.objects.get(pk=request.POST.get("id",""))
					update_data_row.Question = request.POST.get("Question","")
					update_data_row.Bool_overlap = request.POST.get("Bool_overlap","")
					update_data_row.sel_1 = request.POST.get("sel_1","")
					update_data_row.sel_2 = request.POST.get("sel_2","")
					update_data_row.sel_3 = request.POST.get("sel_3","")
					update_data_row.sel_4 = request.POST.get("sel_4","")
					update_data_row.sel_5 = request.POST.get("sel_5","")
					update_data_row.sel_6 = request.POST.get("sel_6","")
					update_data_row.sel_7 = request.POST.get("sel_7","")
					update_data_row.sel_8 = request.POST.get("sel_8","")
					update_data_row.sel_9 = request.POST.get("sel_9","")
					update_data_row.save()
					return redirect("/poll_page_admin/",{'poll_db':poll_db})		
			# request.POST.get("id","") is false? Question Insert
			except:
				form.save()
				return redirect("/poll_page_admin/",{'poll_db':poll_db})
		else:
			return HttpResponse("The data is no valid")
	else:
		return HttpResponse("Request only POST")

def question_update_page(request):
	if request.session.get('username') == 'khanaxbio':
		update_data_id = request.POST.get("data","")
		update_data_row = Poll.objects.get(pk=update_data_id)
		return render(request,"QuestionUpdateForm\\QuestionUpdateForm.html",{'update_data_row':update_data_row})	
	else:
		return render(request,"Wrong_Approach\\Wrong_Approach.html")

def question_delete(request):
	if request.session.get('username') == 'khanaxbio':		
		delete_data_id = request.POST.get("data","")
		delete_data_row = Poll.objects.get(pk=delete_data_id)
		delete_data_row.delete()
		poll_db = Poll.objects.all()
		return redirect('/poll_page_admin/',{'poll_db':poll_db})
	else:
		return render(request,"Wrong_Approach\\Wrong_Approach.html")

def poll_submit(request):
	if request.method == 'POST':
		poll_db=Poll.objects.all()
		get_result_ID = request.session['username']
		get_result_question = []
		get_result_answer = []
		for data in poll_db:
			get_result_question.append(data.Question)
			get_result_answer.append(request.POST.getlist(data.Question))
		Submit_Poll_Table.objects.create(
				Poll_Participant_ID = get_result_ID,
				Poll_Question = get_result_question,
				Poll_Answer = get_result_answer
			)
		return render(request,"Submit_Complete\\Submit_Complete.html")
	else:
		return render(request,"Wrong_Approach\\Wrong_Approach.html")
# Create your views here.
