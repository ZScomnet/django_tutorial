from django.db import models
from django_mysql.models import JSONField

# Create your models here.

SEX_CHOICE = (
	('man','man'),
	('woman,','woman')
)

class Member(models.Model):
	ID = models.CharField(max_length=10, db_column = '아이디')
	Password = models.CharField(max_length=15, db_column = '비밀번호')
	Name = models.CharField(max_length=10, db_column = '이름')
	Birth = models.DateField(auto_now=False, db_column = '생년월일')
	Sex = models.TextField(choices=SEX_CHOICE, db_column = '성별')
	Power = models.BooleanField(default=False, db_column = '관리자 권한')
	Buy_log = JSONField(db_column='구매내역')

	def __str__(self):
		return '%s  -  %s' % (self.Name,self.Birth)

