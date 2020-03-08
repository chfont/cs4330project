from django import forms

from .models import *
class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ('email', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('email', 'fname','lname','phone_number','gender','age','employee_id',)

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Jobpost
        fields = ('job_name','location', 'company_name', 'pay')

class SearchForm(forms.Form):
    location = forms.CharField(label="Location", max_length=64)
    position = forms.CharField(label="Position", max_length=64)