from django.shortcuts import render, redirect
from .forms import *
import MySQLdb as sql
from datetime import date
from .uniqueId import *
db = sql.connect(user="", passwd="",db="") #SET DB CONNECTION BEFORE USE
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
    error = []
    if (request.method == 'POST'):
        form = RegisterForm(request.POST)
        if form.is_valid():
            c.execute("SELECT * FROM login WHERE login.email = %s", (form.cleaned_data['email'],))
            user = c.fetchall()
            if len(user):
                error.append("Email already in use")
            if(form.cleaned_data['password'] != form.cleaned_data['confirm_password']):
                error.append("Passwords do not match")
            if(form.cleaned_data['employee_id'] is not None):
                c.execute("SELECT * from employees where employee_id = %s",(form.cleaned_data['employee_id'],))
                res = c.fetchone()
                if(res is None):
                    error.append("Invalid employee id")
            if(len(error)):
                print(error)
                return render(request, 'register.html', {'form': form, 'errors':error})

            else:
                uid = getUniqueId("users", "id", c,32)
                userDict['id'] = uid
                c.execute("INSERT INTO login(id, email, password) values (%s, %s, %s)", (uid, form.cleaned_data['email'], form.cleaned_data['password']))
                if(form.cleaned_data['employee_id'] is None):
                    c.execute("INSERT INTO users(id, email,fname, lname, phone_number, gender, age) values (%s, %s, %s ,%s, %s, %s, %s, %s)",
                          (uid, form.cleaned_data['email'], form.cleaned_data['fname'], form.cleaned_data['lname'], form.cleaned_data['phone_number'], form.cleaned_data['gender'],
                           form.cleaned_data['age']))
                    db.commit()
                else:
                    c.execute("SELECT * from employees where employee_id = %s",(form.cleaned_data['employee_id'],))
                    c.execute("INSERT INTO users(id, email,fname, lname, phone_number, gender, age, employee_id) values (%s, %s, %s ,%s, %s, %s, %s, %s)",
                              (uid, form.cleaned_data['email'], form.cleaned_data['fname'], form.cleaned_data['lname'], form.cleaned_data['phone_number'], form.cleaned_data['gender'],
                               form.cleaned_data['age'], form.cleaned_data['employee_id']))
                    db.commit()
                return redirect(profile)
    form = RegisterForm()
    return render(request, 'register.html', {'form' : form})

def profile(request):
    if 'id' not in userDict:
        return redirect(login)   
    c.execute("SELECT * FROM users WHERE id = %s", (userDict['id'],))
    user = c.fetchone()
    #User[7] is employee_id
    if(user[7] is not None):
        userDict['employeeID'] = user[7]
        c.execute("SELECT * FROM employees WHERE employee_id = %s", (user[7],))
        employee = c.fetchone()
        if(employee[2] is not None):
            userDict['recruiterID'] = employee[2]
    return render(request, 'profile.html', {'user':user})
def jobsearch(request):
    if 'id' not in userDict:
        redirect(login)
    res = None
    if (request.method == 'POST'):
        form = SearchForm(request.POST)
        if form.is_valid():
            string = "select * from jobpost"
            str = []
            if form.cleaned_data['location'] != '':
                str.append(f"location like '%{form.cleaned_data['location']}%'")
            if form.cleaned_data['position'] != '':
                str.append(f"position like '%{form.cleaned_data['position']}%'")
            if form.cleaned_data['description'] != '':
                str.append(f"description like '%{form.cleaned_data['description']}%'")
            if len(str) > 0:
                string += " where " + str[0]
            if len(str) > 1:
                for i in str[1:]:
                    string += " and " + i
            print(string)
            c.execute(string +" order by post_date")
            res = c.fetchall()
        else:
            c.execute("select * from jobpost")
            res = c.fetchall()
    else:
        c.execute("select * from jobpost")
        res = c.fetchall()
    form = SearchForm()
    return render(request, 'jobsearch.html', {'jobs':res, 'form':form})
def jobpost(request):
    if 'id' not in userDict:
        return redirect(login)
    if 'recruiterID' not in userDict:
        return redirect(profile)
    if(request.method == 'POST'):
        form = JobPostForm(request.POST)
        if form.is_valid():
            new_id = getUniqueId('jobpost', 'job_id', c, 64)
            c.execute("SELECT * FROM companies WHERE company_name = %s", (form.cleaned_data['company_name'],))
            res = c.fetchone()
            if res is None or len(res) == 0: #Company name is invalid
                return redirect(jobpost)
            c.execute("INSERT INTO jobpost(job_id, job_name, location, company_id, company_name, pay, post_date, due_date, recruiter_id, description) VALUES(%s, %s,%s,%s,%s,%s, %s, %s, %s, %s)",
                    (new_id, form.cleaned_data['job_name'], form.cleaned_data['location'],
                        res[0],form.cleaned_data['company_name'],form.cleaned_data['pay'], date.today(), form.cleaned_data['due_date'], userDict['recruiterID'],    form.cleaned_data['description']))
            db.commit()

        
    form = JobPostForm()
    return render(request, 'jobpost.html', {'form':form})
