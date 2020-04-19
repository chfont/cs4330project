from django.shortcuts import render, redirect
from .forms import *
import MySQLdb as sql
from datetime import date, datetime
from .uniqueId import *
from django.views.generic import TemplateView
from .dbQuery import *
from django.core.files.storage import FileSystemStorage
import os

db = sql.connect(user="django4330", passwd="qd0bQues0",db="cs4330")
cursor = db.cursor()

db_obj = DBObject(db, cursor)

userDict = {}   # dictionary to store current user info for quick usage


# Function to handle login requests
def login(request):
    userDict.clear()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = checkLogin(db_obj, form.cleaned_data['email'], form.cleaned_data['password'])
            if len(user):
                # If this fails, the user was not found
                userDict['id'] = user[0][2]
                return redirect(profile)
    form = LoginForm()
    return render(request, 'login.html', {'form' : form})

# Function to handle Admin Login page
def adminLogin(request):
    userDict.clear()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = checkAdmin(db_obj, form.cleaned_data['email'], form.cleaned_data['password'])
            if user is not None and len(user):
                userDict['admin'] = 'admin'
                return redirect(admin_home)
    form = LoginForm()
    return render(request, 'admin_login.html', {'form' : form})

# Function to handle registration requests
def register(request):
    error = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = findExistingUser(db_obj, form.cleaned_data['email'])
            if len(user):
                error.append("Email already in use")
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                error.append("Passwords do not match")
            if form.cleaned_data['employee_id'] is not None and form.cleaned_data['employee_id'] != '':
                res = findValidEmployee(db_obj,form.cleaned_data['employee_id'])
                if res is None:
                    error.append("Invalid employee id")
            if len(error):
                return render(request, 'register.html', {'form': form, 'errors':error})

            else:
                uid = getUniqueId("users", "id", cursor, 32)
                userDict['id'] = uid
                if form.cleaned_data['employee_id'] is None or form.cleaned_data['employee_id'] is '':
                    addNonEmployeeUser(db_obj, (uid, form.cleaned_data['email'], form.cleaned_data['password']),
                    (uid, form.cleaned_data['email'], form.cleaned_data['fname'], form.cleaned_data['lname'], form.cleaned_data['phone_number'], form.cleaned_data['gender'],
                                        form.cleaned_data['age']))
                else:
                    addEmployeeUser(db_obj, (uid, form.cleaned_data['email'], form.cleaned_data['password']),
                                    (uid, form.cleaned_data['email'], form.cleaned_data['fname'], form.cleaned_data['lname'], form.cleaned_data['phone_number'], form.cleaned_data['gender'],
                                     form.cleaned_data['age'], form.cleaned_data['employee_id']))
                return redirect(profile)
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# Function to handle profile page requests
def profile(request):
    if 'id' not in userDict:
        return redirect(login)
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            if doesNotHaveSkill(db_obj, userDict['id'], form.cleaned_data['skill'].upper()):
                addSkillToUser(db_obj, userDict['id'], form.cleaned_data['skill'].upper())
        else:
            if 'resume' in request.FILES:
                uploaded_file = request.FILES['resume']
                file_name = userDict['id'] + 'resume.pdf'
                file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media\\') + file_name
                fs = FileSystemStorage()
                if fs.exists(file_path):
                    fs.delete(file_path)
                fs.save(file_name, uploaded_file)

    user = getUserById(db_obj, userDict['id'])

    # Store user name info
    userDict['firstname'] = user[2]
    userDict['lastname'] = user[3]

    # User[7] is employee_id
    if user[7] is not None:
        userDict['employeeID'] = user[7]
        employee = getEmployeeInfo(db_obj, user[7])
        if employee[2] is not None:
            userDict['recruiterID'] = employee[2]
    employeeID = None
    if 'employeeID' in userDict:
        employeeID = userDict['employeeID']
    recruiterID = None
    if 'recruiterID' in userDict:
        recruiterID = userDict['recruiterID']
    apps = getJobApplicationsOfUser(db_obj, userDict['id'])
    form = SkillForm()
    skills = getSkillsOfUser(db_obj, userDict['id'])
    return render(request, 'profile.html', {'user': user, 'employee': employeeID, 'apps': apps, 'recruiter':recruiterID, 'skillform':form, 'skills':skills})


# Function to handle job search page requests
def jobsearch(request):
    if 'id' not in userDict:
        redirect(login)
    res = None
    if request.method == 'POST':
        form = SearchApplyForm(request.POST)
        if form.is_valid():
            userDict['job_id'] = form.cleaned_data['job_id']
            return redirect(apply)
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
            cursor.execute(string + " order by post_date")
            res = cursor.fetchall()

        else:
            cursor.execute("select * from jobpost")
            res = cursor.fetchall()
    else:
        cursor.execute("select * from jobpost")
        res = cursor.fetchall()
    form = SearchForm()
    idform = SearchApplyForm()
    return render(request, 'jobsearch.html', {'jobs':res, 'form':form, 'idform':idform})


# Function to handle job posting page requests
def jobpost(request):
    if 'id' not in userDict:
        return redirect(login)
    if 'recruiterID' not in userDict:
        return redirect(profile)
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            new_id = getUniqueId('jobpost', 'job_id', cursor, 64)
            res = getCompany(db_obj, form.cleaned_data['company_name'])
            if res is None or len(res) == 0:  # Company name is invalid
                #TODO: Error Message here
                return redirect(jobpost)
            cursor.execute("INSERT INTO jobpost(job_id, job_name, location, company_id, company_name, pay, post_date, due_date, recruiter_id, description, long_description, requirements) VALUES(%s, %s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)",
                           (new_id, form.cleaned_data['job_name'], form.cleaned_data['location'],
                        res[0],form.cleaned_data['company_name'],form.cleaned_data['pay'], date.today(), form.cleaned_data['due_date'], userDict['recruiterID'],    form.cleaned_data['description'], form.cleaned_data['long_description'], form.cleaned_data['requirements']))
            db.commit()

    form = JobPostForm()
    return render(request, 'jobpost.html', {'form':form})


# Function to handle message page requests
def messages(request):
    if 'id' not in userDict:
        return redirect(login)
    err = None
    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            cursor.execute("SELECT * FROM users WHERE  fname = %s and lname = %s", (form.cleaned_data['first_name'], form.cleaned_data['last_name']))
            res = cursor.fetchall()
            if res is None or len(res) == 0:  # Company name is invalid
                err = ["Person not found, please try again"]
            else:
                new_id = getUniqueId('messages', 'message_id', cursor, 32)
                cursor.execute("INSERT INTO messages(message_id, sender_id, receiver_id, message, time) VALUES(%s, %s, %s, %s, %s)", (new_id, userDict['id'], res[0][0], form.cleaned_data['message'], datetime.datetime.now()))
                db.commit()
    form = NewMessageForm()

    # get received messages
    cursor.execute("SELECT sender_id, time, message FROM messages WHERE receiver_id = %s ORDER BY time desc", (userDict['id'],))
    receivers = cursor.fetchall()
    cursor.execute("SELECT receiver_id, time, message FROM messages WHERE sender_id = %s ORDER BY time desc", (userDict['id'],))
    senders = cursor.fetchall()
    rec_ids = [x[0] for x in receivers]
    receivers = [x for x in receivers]
    senders = [x for x in senders if x[0] not in rec_ids]
    res = receivers + senders
    rec_names = None

    # Map user names to user ids
    for result in res:
        cursor.execute("select fName, lName from users where id = %s", (result[0],))
        n = cursor.fetchone()
        print(n[0])
        print(result[1])

        if rec_names is None:
            rec_names = [(n[0], n[1], result[1], result[2])]
        else:
            rec_names += [(n[0], n[1], result[1], result[2])]

    # get sent messages
    cursor.execute("SELECT receiver_id, time, message FROM messages WHERE sender_id = %s ORDER BY time desc", (userDict['id'],))
    receivers = cursor.fetchall()
    cursor.execute("SELECT sender_id, time, message FROM messages WHERE receiver_id = %s ORDER BY time desc", (userDict['id'],))
    senders = cursor.fetchall()
    rec_ids = [x[0] for x in receivers]
    receivers = [x for x in receivers]
    senders = [x for x in senders if x[0] not in rec_ids]
    res = receivers + senders
    sent_names = None

    
    for result in res:
        cursor.execute("select fName, lName from users where id = %s", (result[0],))
        n = cursor.fetchone()
        print(n[0])
        print(result[1])

        if sent_names is None:
            sent_names = [(n[0], n[1], result[1], result[2])]
        else:
            sent_names += [(n[0], n[1], result[1], result[2])]
    return render(request, 'message.html', {'messages': res, 'rec_names':rec_names, 'sent_names':sent_names,'form': form, 'errors':err, 'length': len(res)})

def apply(request):
    if 'id' not in userDict:
        return redirect(login)
    if 'job_id' not in userDict:
        redirect(jobsearch)
    err = None
    success = False
    if request.method == 'POST':
        form = SearchApplyForm(request.POST)
        if form.is_valid():
            if not isUniqueApplication(db_obj, userDict['id'], form.cleaned_data['job_id']):
                err = ["Already applied to this job"]
            else:
                if getApplicationCountByUser(db_obj, userDict['id']) == 20:
                    err = ["Maximum application count reached (20)."]
                else:
                    app_id = getUniqueId("applications", "application_id", cursor, 32)
                    addApplicationToTable(db_obj, app_id, form.cleaned_data['job_id'], userDict['id'])
                    success = True
        else:
            err = ["Unexpected Error occurred, please try again"]
    job_id = userDict['job_id']
    post = getJobPost(db_obj, job_id)

    # This should never happen, but a fail-safe is necessary
    if post is None:
        redirect(jobsearch)
    requirements = (post[11]).split(',')
    if post[10] is None:
        long_desc = "None Given"
    else:
        long_desc = post[10]
    form = SearchApplyForm()
    return render(request, 'apply.html', {'post':post, 'long_desc': long_desc, 'requirements': requirements, 'form':form, 'succeed':success, 'errors':err})


def recruiter_post(request):
    if 'id' not in userDict:
        return redirect(login)
    if 'recruiterID' not in userDict:
        return redirect(profile)
    if request.method == 'POST':
        form = SearchApplyForm(request.POST)
        if form.is_valid():
            userDict['job_id'] = form.cleaned_data['job_id']
            return redirect(view_apps)


    idform = SearchApplyForm()
    job_posts = getJobPostsByRecruiter(db_obj, userDict['recruiterID'])
    return render(request, 'recruiter_post.html', {'posts':job_posts, 'idform':idform})


def admin_home(request):
    if 'admin' not in userDict:
        return redirect(adminLogin)
    stats = getJobStatistics(db_obj)
    jobappsTotal = stats[0][0]
    jobPostsTotal = stats[1][0]
    postsPerCompany = stats[2]
    appsPerCompany = stats[3]
    users = stats[4][0]
    return render(request, 'admin_home.html', {'appsTotal': jobappsTotal, 'postTotal': jobPostsTotal, 'companyPosts': postsPerCompany, 'companyApps':appsPerCompany, 'users':users})

def view_apps(request):
    if 'id' not in userDict:
        return redirect(login)
    if 'recruiterID' not in userDict:
        return redirect(profile)

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST)
        if form.is_valid():
            updateApplication(db_obj, form.cleaned_data['app_id'], form.cleaned_data['status'])
    applicants = getJobApplicants(db_obj, userDict['job_id'])

    stitched = []
    resArr = []
    for applicant in applicants:
        id = applicant[5]
        skills = getSkillsOfUser(db_obj, id)
        file_path = 'http://127.0.0.1:8000/media/'
        resume = file_path + id + 'resume.pdf'
        stitched.append([applicant, skills, resume])
    form = ApplicationStatusForm()
    return render(request, 'viewapp.html', {'applicants': stitched, 'form': form})