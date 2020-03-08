from django.shortcuts import render, redirect
from .forms import *
import MySQLdb as sql 
import random
import string
db = sql.connect(user="django4330", passwd="qd0bQues0",db="cs4330")
c = db.cursor()

userDict = {}

def login(request):
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            c.execute("SELECT * FROM login WHERE login.email = %s and login.password = %s", (form.cleaned_data['email'], form.cleaned_data['password']))
            user = c.fetchall()
            if len(user):
                # this is good
                userDict['id'] = user[0][2]
                return redirect(profile)
    form = LoginForm()
    return render(request, 'login.html', {'form' : form})

def register(request):
    form = RegisterForm()
    return render(request, 'register.html', {'form' : form})

def profile(request):
    if 'id' not in userDict:
        return redirect(login)   
    c.execute("SELECT * FROM users WHERE id = %s", (userDict['id'],))
    user = c.fetchone()
    # user[9] is recruiter_id
    if user[9] is not None:                 
        userDict['recruiterID'] = user[9]
    return render(request, 'profile.html', {'user':user})
def jobsearch(request):
    if 'id' not in userDict:
        redirect(login)
    c.execute("select * from jobpost")
    res = c.fetchall()
    return render(request, 'jobsearch.html', {'jobs':res})
def jobpost(request):
    if 'id' not in userDict:
        return redirect(login)
    if 'recruiterID' not in userDict:
        return redirect(profile)
    if(request.method == 'POST'):
        form = JobPostForm(request.POST)
        if form.is_valid():
            new_id =''.join(random.choices(string.ascii_lowercase + string.digits, k=64))
            c.execute("SELECT * FROM jobpost where job_id = %s", (new_id,))
            res = c.fetchone()
            while res is not None and len(res) > 0:   #ID collision
                new_id =''.join(random.choices(string.ascii_lowercase + string.digits, k=64))
                c.execute("SELECT * FROM jobpost where job_id = %s", (new_id))
                res = c.fetchone()
            c.execute("SELECT * FROM companies WHERE company_name = %s", (form.cleaned_data['company_name'],))
            res = c.fetchone()
            print(res)
            if res is None or len(res) == 0: #Company name is invalid
                return redirect(jobpost)
            print("HERE")
            c.execute("INSERT INTO jobpost(job_id, job_name, location, company_id, company_name, pay) VALUES(%s, %s,%s,%s,%s,%s)", 
                    (new_id, form.cleaned_data['job_name'], form.cleaned_data['location'],
                        res[0],form.cleaned_data['company_name'],form.cleaned_data['pay'],))
            db.commit()

        
    form = JobPostForm()
    return render(request, 'jobpost.html', {'form':form})
