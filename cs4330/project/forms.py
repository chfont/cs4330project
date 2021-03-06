from django import forms

from .models import *


class LoginForm(forms.Form):
    email = forms.CharField(label="Login/Email", max_length=64)
    password = forms.CharField(label="Password",max_length=128, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.CharField(label="Email", max_length=64)
    fname = forms.CharField(label="First Name",max_length=64)
    lname = forms.CharField(label="Last Name",max_length=64)
    phone_number = forms.IntegerField(label="Phone Number",required=False)
    gender = forms.CharField(label="Gender",max_length=1, required=False)
    age = forms.IntegerField(label="Age",required=False)
    employee_id = forms.CharField(label="Employee ID",max_length=32, required=False)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    widgets = {
        'password': forms.PasswordInput(),
        'confirm_password': forms.PasswordInput(),
    }


class JobPostForm(forms.Form):
    job_name = forms.CharField(label="Job Title", max_length=64)
    location = forms.CharField(label="Location", max_length=64)
    company_name = forms.CharField(label="Company Name", max_length=64)
    pay = forms.DecimalField(label="Pay Rate", min_value= 0.0, decimal_places=3)
    due_date = forms.DateField(label="Application Due Date")
    description = forms.CharField(label="Description (Max 500 characters)",required=True,
                                  widget=forms.Textarea(attrs={'cols': 30, 'rows': 10}))
    long_description = forms.CharField(label="Long Description (Max 5000 characters)", required=False,
                                       widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))
    requirements = forms.CharField(label="Requirements (Comma-separated list", required=True,
                                   widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))


class SearchForm(forms.Form):
    location = forms.CharField(label="Location", max_length=64, required=False)
    position = forms.CharField(label="Position", max_length=64, required=False)
    description = forms.CharField(label="Description contains", max_length=1000, required=False)


class NewMessageForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=64)
    last_name = forms.CharField(label="Last Name", max_length=64)
    message = forms.CharField(label="Message", max_length=1000)

#Hidden form to be used internally by javascript for the job search page
class SearchApplyForm(forms.Form):
    job_id = forms.CharField(label="Job Id", max_length=64)

class SkillForm(forms.Form):
    skill = forms.CharField(label="Skill", max_length=32)

class ApplicationStatusForm(forms.Form):
    app_id = forms.CharField(label="Application Id", max_length=32)
    status = forms.CharField(label="Status", max_length=10)