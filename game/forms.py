from django.forms import ModelForm
from django import forms
from EA.game.models import Game

class GameForm(ModelForm):
	class Meta:
		model = Game
		fields = ('name', )
		
class TestForm(forms.Form):
	name = forms.CharField(max_length=100)
	testvalue = forms.BooleanField()