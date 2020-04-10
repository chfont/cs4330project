from django.shortcuts import render, redirect
from .forms import *
import MySQLdb as sql
from datetime import date, datetime
from .uniqueId import *
from django.views.generic import TemplateView
from .upload import *


db = sql.connect(user="django4330", passwd="qd0bQues0",db="cs4330")
c = db.cursor()

userDict = {}   # dictionary to store current user info for quick usage


# Function to handle login requests
def login(request):
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            c.execute("SELECT * FROM login WHERE login.email = %s and login.password = %s", (form.cleaned_data['email'], form.cleaned_data['password']))
            user = c.fetchall()
            if len(user):
                # If this fails, the user was not found
                userDict['id'] = user[0][2]
                return redirect(profile)
    form = LoginForm()
    return render(request, 'login.html', {'form' : form})

# Function to handle registration requests
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
            if(form.cleaned_data['employee_id'] is not None and form.cleaned_data['employee_id'] is not ''):
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
                if(form.cleaned_data['employee_id'] is None or form.cleaned_data['employee_id'] is ''):
                    c.execute("INSERT INTO users(id, email,fname, lname, phone_number, gender, age) values (%s, %s, %s ,%s, %s, %s, %s)",
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

# Function to handle profile page requests
def profile(request):
    if 'id' not in userDict:
        return redirect(login) 
    
    if request.method == 'POST':
        upload(request.FILES['resume'])

      
    c.execute("SELECT * FROM users WHERE id = %s", (userDict['id'],))
    user = c.fetchone()



    # Store user name info
    userDict['firstname'] = user[2]
    userDict['lastname'] = user[3]

    #User[7] is employee_id
    if(user[7] is not None):
        userDict['employeeID'] = user[7]
        c.execute("SELECT * FROM employees WHERE employee_id = %s", (user[7],))
        employee = c.fetchone()
        if(employee[2] is not None):
            userDict['recruiterID'] = employee[2]
    employeeID = None
    if 'employeeID' in userDict:
        employeeID = userDict['employeeID']
    return render(request, 'profile.html', {'user':user, 'employee': employeeID})

# Function to handle job search page requests
def jobsearch(request):
    if 'id' not in userDict:
        redirect(login)
    res = None
    if (request.method == 'POST'):
        form = SearchForm(request.POST)
        if form.is_valid():
            string = "select * from jobpost"
            str = []

            # if chain to modify query for filtering
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

# Function to handle job posting page requests
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
            if res is None or len(res) == 0:  # Company name is invalid
                return redirect(jobpost)
            c.execute("INSERT INTO jobpost(job_id, job_name, location, company_id, company_name, pay, post_date, due_date, recruiter_id, description) VALUES(%s, %s,%s,%s,%s,%s, %s, %s, %s, %s)",
                    (new_id, form.cleaned_data['job_name'], form.cleaned_data['location'],
                        res[0],form.cleaned_data['company_name'],form.cleaned_data['pay'], date.today(), form.cleaned_data['due_date'], userDict['recruiterID'],    form.cleaned_data['description']))
            db.commit()

        
    form = JobPostForm()
    return render(request, 'jobpost.html', {'form':form})

# Function to handle message page requests
def messages(request):
    if 'id' not in userDict:
        return redirect(login)
    err = None
    if(request.method == 'POST'):
        form = NewMessageForm(request.POST)
        if form.is_valid():
            c.execute("SELECT * FROM users WHERE  fname = %s and lname = %s", (form.cleaned_data['first_name'], form.cleaned_data['last_name']))
            res = c.fetchall()
            if res is None or len(res) == 0:  # Company name is invalid
                err = ["Person not found, please try again"]
            else:
                new_id = getUniqueId('messages', 'message_id', c, 32)
                c.execute("INSERT INTO messages(message_id, sender_id, receiver_id, message, time) VALUES(%s, %s, %s, %s, %s)", (new_id, userDict['id'], res[0][0], form.cleaned_data['message'],  datetime.now()))
                db.commit()
    form = NewMessageForm()

    # get all conversations, and the other individual's name
    c.execute("SELECT receiver_id, time, message FROM messages WHERE sender_id = %s", (userDict['id'],))
    receivers = c.fetchall()
    c.execute("SELECT sender_id, time, message FROM messages WHERE receiver_id = %s", (userDict['id'],))
    senders = c.fetchall()
    rec_ids = [x[0] for x in receivers]
    receivers = [x for x in receivers]
    senders = [x for x in senders if x[0] not in rec_ids]
    res = receivers + senders
    names = None

    # Map user names to user ids
    for result in res:
        c.execute("select fName, lName from users where id = %s", (result[0],))
        n = c.fetchone()
        print(n[0])
        print(result[1])
        if names is None:
            names = [(n[0], n[1], result[1], result[2])]
        else:
            names += [(n[0], n[1], result[1], result[2])]
    return render(request, 'message.html', {'messages': res, 'names':names,'form': form, 'errors':err, 'length': len(res)})


