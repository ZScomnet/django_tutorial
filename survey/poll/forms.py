from django import forms
from .models import Poll,Submit_Poll_Table

class Pollform(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ('Question','Bool_overlap','sel_1','sel_2','sel_3','sel_4',
			'sel_5','sel_6','sel_7','sel_8','sel_9')

class Submitform(forms.ModelForm):
	class Meta:
		model = Submit_Poll_Table
		fields = ('Poll_Participant_ID','Poll_Question','Poll_Answer',)