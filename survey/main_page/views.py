from django.shortcuts import render,HttpResponse
from poll import models
# Create your views here.

def main_page(request): # 메인 화면
	return render(request,"main\\main.html")

def review_page_User(request): # 유저의 리뷰 리스트
	Submit_Poll_Table_db = models.Submit_Poll_Table.objects.all()
	return render(request,"Review_User\\Review_User.html",{'Submit_Poll_Table_db' : Submit_Poll_Table_db})

def review_page_User_Detail(request,No): # 유저의 리스트 클릭시 나오는 페이지
	Submit_Poll_Table_db = models.Submit_Poll_Table.objects.get(pk=No)
	context = list(zip(Submit_Poll_Table_db.Poll_Question,Submit_Poll_Table_db.Poll_Answer))
	price = 0
	for data in Submit_Poll_Table_db.Poll_Result:
		price += int(data[2])
	total_data = { 
	'ID' : Submit_Poll_Table_db.Poll_Participant_ID,
	'Question_and_Answer' : context,
	'Date' : Submit_Poll_Table_db.Poll_date,
	'Admin_Answer' : Submit_Poll_Table_db.Admin_Answer,
	'Poll_Result' : Submit_Poll_Table_db.Poll_Result,
	'price' : price}
	if request.session['username'] != Submit_Poll_Table_db.Poll_Participant_ID:
		return render(request,"Wrong_Approach\\Wrong_Approach.html")
	else:
		return render(request,"Review_User\\Review_User_Click.html",{'total_data':total_data})

def review_page_Admin(request): # 관리자의 리뷰 리스트
	Submit_Poll_Table_db = models.Submit_Poll_Table.objects.all()
	return render(request,"Review_Admin\\Review_Admin.html",{'Submit_Poll_Table_db' : Submit_Poll_Table_db})

def review_page_Admin_Detail(request,No): # 관리자의 리스트 클릭시 나오는 페이지
	Submit_Poll_Table_db = models.Submit_Poll_Table.objects.get(pk=No)
	context = list(zip(Submit_Poll_Table_db.Poll_Question,Submit_Poll_Table_db.Poll_Answer))
	total_data = { 
	'ID' : Submit_Poll_Table_db.Poll_Participant_ID,
	'Question_and_Answer' : context,
	'Date' : Submit_Poll_Table_db.Poll_date,
	'Admin_Answer' : Submit_Poll_Table_db.Admin_Answer,
	'pk' : No }
	if request.session['username'] != 'khanaxbio':
		return render(request,"Wrong_Approach\\Wrong_Approach.html")
	else:
		return render(request,"Review_Admin\\Review_Admin_Click.html",{'total_data':total_data})

def review_update(request,No):
	if request.method == 'POST':
		Submit_Poll_Table_db = models.Submit_Poll_Table.objects.get(pk=No)
		Submit_Poll_Table_db.Admin_Answer = request.POST.get("Answer","")
		Submit_Poll_Table_db.Poll_Result = []
		if request.POST.get("med_1") != None and request.POST.get("med_1") != '':
			context = []
			context.append(request.POST.get("med_1"))
			context.append(request.POST.get("med_1_time"))
			context.append(request.POST.get("med_1_price"))
			Submit_Poll_Table_db.Poll_Result.append(context)
			del context
		if request.POST.get("med_2") != None and request.POST.get("med_2") != '':
			context = []
			context.append(request.POST.get("med_2"))
			context.append(request.POST.get("med_2_time"))
			context.append(request.POST.get("med_2_price"))
			Submit_Poll_Table_db.Poll_Result.append(context)
			del context
		if request.POST.get("med_3") != None and request.POST.get("med_3") != '':
			context = []
			context.append(request.POST.get("med_3"))
			context.append(request.POST.get("med_3_time"))
			context.append(request.POST.get("med_3_price"))
			Submit_Poll_Table_db.Poll_Result.append(context)
			del context
		if request.POST.get("med_4") != None and request.POST.get("med_4") != '':
			context = []
			context.append(request.POST.get("med_4"))
			context.append(request.POST.get("med_4_time"))
			context.append(request.POST.get("med_4_price"))
			Submit_Poll_Table_db.Poll_Result.append(context)
			del context
		if request.POST.get("med_5") != None and request.POST.get("med_5") != '':
			context = []
			context.append(request.POST.get("med_5"))
			context.append(request.POST.get("med_5_time"))
			context.append(request.POST.get("med_5_price"))
			Submit_Poll_Table_db.Poll_Result.append(context)
			del context
		if request.POST.get("med_6") != None and request.POST.get("med_6") != '':
			context = []
			context.append(request.POST.get("med_6"))
			context.append(request.POST.get("med_6_time"))
			context.append(request.POST.get("med_6_price"))
			Submit_Poll_Table_db.Poll_Result.append(context)
			del context
		Submit_Poll_Table_db.save()
		return render(request,"Update_Complete\\Update_Complete.html")
	else:
		return render(request,"Wrong_Approach\\Wrong_Approach.html")