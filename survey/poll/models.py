from django.db import models
from django_mysql.models import JSONField
# from django_mysql.models import ListCharField

class Poll(models.Model):
	Question = models.CharField(max_length=200,db_column='질문')
	Bool_overlap = models.BooleanField(default=False)
	sel_1 = models.CharField(max_length=15,db_column='보기1')
	sel_2 = models.CharField(max_length=15,db_column='보기2')
	sel_3 = models.CharField(max_length=15,db_column='보기3',null=True,blank=True,default='')
	sel_4 = models.CharField(max_length=15,db_column='보기4',null=True,blank=True,default='')
	sel_5 = models.CharField(max_length=15,db_column='보기5',null=True,blank=True,default='')
	sel_6 = models.CharField(max_length=15,db_column='보기6',null=True,blank=True,default='')
	sel_7 = models.CharField(max_length=15,db_column='보기7',null=True,blank=True,default='')
	sel_8 = models.CharField(max_length=15,db_column='보기8',null=True,blank=True,default='')
	sel_9 = models.CharField(max_length=15,db_column='보기9',null=True,blank=True,default='')

	def __str__(self):
		return self.Question

class Submit_Poll_Table(models.Model):
	Poll_Participant_ID = models.CharField(max_length=15,db_column='작성자')
	Poll_Question = JSONField(db_column='질문')
	Poll_Answer = JSONField(db_column='답변')
	Poll_date = models.DateField(auto_now=True,db_column='등록날짜')
	Admin_Answer = models.TextField(null=True,blank=True,db_column='관리자답변')
	Poll_Result = JSONField(db_column='처방제품')

	def __str__(self):
		return '%s 님의 설문조사' % (self.Poll_Participant_ID)

class Poll_Detail(models.Model):
	Poll_Participant_ID = models.CharField(max_length=15,db_column='상담자') # 아이디
	Poll_Condition = JSONField(db_column='상세상담조건') # 나이 직업 증상
	Poll_Question = JSONField(db_column='질문')
	Bool_overlap = models.BooleanField(default=False)
	Poll_Selection = JSONField(db_column='보기')
	Poll_Answer = JSONField(db_column='답변')
	Poll_date = models.DateField(auto_now=True,db_column='등록날짜')
	Admin_Answer = models.TextField(null=True,blank=True,db_column='관리자답변')
	Poll_Result = JSONField(db_column='처방내용')
# # Create your models here.
