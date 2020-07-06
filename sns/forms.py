from django import forms
from.models import Message,Group,Friend,Good
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['owner','group','content']
