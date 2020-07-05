from django import forms
from.models import Friend, Message

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['name','mail','gender','age','birthday']

class HelloForm(forms.Form):
    name = forms.CharField(label='Name')
    mail = forms.EmailField(label='Email')
    gender = forms.BooleanField(label='Gender',required=False)
    age = forms.IntegerField(label='Age')
    birthday = forms.DateField(label='Birth')

class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False)

class CheckForm(forms.Form):
    empty = forms.CharField(label='Empty', empty_value=True)
    min = forms.CharField(label='Min', min_length=10)
    max = forms.CharField(label='Max', max_length=10)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content', 'friend']
