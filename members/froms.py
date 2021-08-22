from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    first_name  = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))


    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password1","password2")
        labels = {
            'Username': '',
            'First name': '',
            'Last name': '',
            'Email': '',
            'Password1': '',
            'Password2': '',
        }


    def __init__(self, *arg, **kwargs):
        super(RegisterUserForm,self).__init__(*arg, **kwargs)
        self.fields["password1"].widget.attrs["class"] = 'form-control'
        self.fields["password2"].widget.attrs["class"] = 'form-control'


