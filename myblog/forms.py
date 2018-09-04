from django import forms 

from .models import *
from pagedown.widgets import PagedownWidget
class PostForm(forms.ModelForm):
	content=forms.CharField(widget=PagedownWidget(show_preview=False))
	publish=forms.DateField(widget=forms.SelectDateWidget)
	tag=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all())
	class Meta:
		
		model=Post
		fields=["title","content","image","draft","publish","tag"]