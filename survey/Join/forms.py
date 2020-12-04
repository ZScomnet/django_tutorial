from django import forms
from django.contrib.auth.models import User
from .models import Member

class Postform(forms.ModelForm):
	class Meta:
		model = Member
		fields = ('ID','Password','Name','Birth','Sex',)

class Loginform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','password']