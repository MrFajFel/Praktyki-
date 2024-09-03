from django import forms
from app.models import User

class LogForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','computer')
