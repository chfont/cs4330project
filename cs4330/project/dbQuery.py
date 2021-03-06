# Database queries are here, to remove clutter from views
import datetime

class DBObject:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

# Query for login
def checkLogin(db_obj, email, password):
    db_obj.cursor.execute("SELECT * FROM login WHERE login.email = %s and login.password = %s", (email, password))
    return db_obj.cursor.fetchall()

# Check if email is taken
def findExistingUser(db_obj, email):
    db_obj.cursor.execute("SELECT * FROM login WHERE login.email = %s", (email,))
    return db_obj.cursor.fetchall()

# Determine if the employee with this id exists
def findValidEmployee(db_obj, employee_id):
    db_obj.cursor.execute("SELECT * from employees where employee_id = %s", (employee_id,))
    return db_obj.cursor.fetchone()

# Add user without employee id
def addNonEmployeeUser(db_obj, login_tuple, user_tuple):
    db_obj.cursor.execute("INSERT INTO login(id, email, password) values (%s, %s, %s)", (login_tuple[0], login_tuple[1], login_tuple[2]))
    db_obj.cursor.execute("INSERT INTO users(id, email,fname, lname, phone_number, gender, age) values (%s, %s, %s ,%s, %s, %s, %s)",
                          (user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[3], user_tuple[4], user_tuple[5],user_tuple[6]))
    db_obj.db.commit()

# Add user with employee id
def addEmployeeUser(db_obj, login_tuple, user_tuple):
    db_obj.cursor.execute("INSERT INTO login(id, email, password) values (%s, %s, %s)", (login_tuple[0], login_tuple[1], login_tuple[2]))
    db_obj.cursor.execute("INSERT INTO users(id, email,fname, lname, phone_number, gender, age, employee_id) values (%s, %s, %s ,%s, %s, %s, %s, %s)",
                          (user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[3], user_tuple[4], user_tuple[5],user_tuple[6], user_tuple[7]))
    db_obj.db.commit()


# Get user info via id
def getUserById(db_obj, id):
    db_obj.cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    return db_obj.cursor.fetchone()

# Get user's job applications
def getJobApplicationsOfUser(db_obj, id):
    db_obj.cursor.execute("SELECT status, job_name, company_name FROM applications, jobpost where applications.user_id = %s and applications.job_id = jobpost.job_id", (id,))
    return db_obj.cursor.fetchall()

# Get info of employee based on id
def getEmployeeInfo(db_obj, employee_id):
    db_obj.cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    return db_obj.cursor.fetchone()

# Get job post info based on id
def getJobPost(db_obj, job_id):
    db_obj.cursor.execute("select * from jobpost where job_id = %s", (job_id,))
    return db_obj.cursor.fetchone()

# Get company info based on name
def getCompany(db_obj, company_name):
    db_obj.cursor.execute("SELECT * FROM companies WHERE company_name = %s", (company_name,))
    return db_obj.cursor.fetchone()

# Verifies that user has not applied to this job
def isUniqueApplication(db_obj, user_id, job_id):
    db_obj.cursor.execute("select * from applications where job_id = %s and user_id = %s", (job_id, user_id))
    results = db_obj.cursor.fetchall()
    return len(results) == 0

# Figure out how many applications a user has sent
# Only counts submitted applications, rejected/accepted applications do not count against total
def getApplicationCountByUser(db_obj, user_id):
    db_obj.cursor.execute("select count(*) from applications where user_id = %s and status = 'SUBMITTED'", (user_id,))
    results = db_obj.cursor.fetchone()
    return results[0]

# Add application to a job for a specific user
def addApplicationToTable(db_obj, app_id, job_id, user_id):
    db_obj.cursor.execute("insert into applications(application_id, job_id, user_id, status, submission_time) values(%s, %s, %s, %s, %s)", (app_id, job_id, user_id, 'SUBMITTED', datetime.datetime.now()))
    db_obj.db.commit()
    return True

# Get all job posts from specified recruiter
def getJobPostsByRecruiter(db_obj, rec_id):
    db_obj.cursor.execute("select * from jobpost where recruiter_id = %s", (rec_id,))
    return db_obj.cursor.fetchall()

# Determine if user has skill or not
def doesNotHaveSkill(db_obj, user_id, skill):
    db_obj.cursor.execute("select * from user_skills where user_id = %s and skill = %s", (user_id, skill))
    res = db_obj.cursor.fetchall()
    return len(res) == 0

# Add skill to user
def addSkillToUser(db_obj, user_id, skill):
    db_obj.cursor.execute("insert into user_skills(user_id, skill) values(%s, %s)", (user_id, skill))
    db_obj.db.commit()

# Get skills of specific user
def getSkillsOfUser(db_obj, user_id):
    db_obj.cursor.execute("select skill from user_skills where user_id = %s",(user_id,) )
    return db_obj.cursor.fetchall()

# Checks login into admin page
def checkAdmin(db_obj, username, password):
    db_obj.cursor.execute("select * from admin_login where id = %s and password = %s",(username, password))
    return db_obj.cursor.fetchone()

# Generates administrative statistics
def getJobStatistics(db_obj):
    date = datetime.datetime.now()
    # modify date to point to previous month
    if date.month == 1:
        date = date.replace(year=date.year-1)
        date=date.replace(month=12)
    else:
        date=date.replace(month=date.month - 1)
    # get application count in previous month
    db_obj.cursor.execute("select count(*) from applications where submission_time > %s",(date,))
    jobApplicationsSent = db_obj.cursor.fetchall()
    # get job post count made in previous month
    db_obj.cursor.execute("select count(*) from jobpost where post_date > %s", (date,))
    jobpostsMade = db_obj.cursor.fetchall()
    # get job post count made in previous month by company
    db_obj.cursor.execute('''Select companies.company_name, 
    ifnull(a.count_jobs,0) from companies 
    left join (select jobpost.company_name, count(*) as count_jobs from jobpost where post_date>%s group by jobpost.company_name) a on a.company_name= companies.company_name''', (date,))
    postsByCompany = db_obj.cursor.fetchall()
    # get application count in previous month by company
    db_obj.cursor.execute('''
    select companies.company_name, ifnull(a.count,0) from companies
    left join (
        select company_name, count(*) as count from jobpost, applications where jobpost.job_id = applications.job_id and applications.submission_time
        > %s group by company_name    
    ) a on a.company_name = companies.company_name
    ''', (date,))
    applicationsPerCompany = db_obj.cursor.fetchall()
    # get total user count
    db_obj.cursor.execute('''select count(*) from login''')
    userCount = db_obj.cursor.fetchall()
    return [jobApplicationsSent, jobpostsMade, postsByCompany, applicationsPerCompany, userCount]

# get and sort job applications by employee status and skill count
def getJobApplicants(db_obj, job_id):
    #these queries join three tables for necessary information
    db_obj.cursor.execute('''Select *, ifnull(a.skill_ct,0) from applications left join (select *, ifnull(s.skill_ct,0) from users left join (select count(*) as skill_ct, user_id from user_skills group by user_id) s on s.user_id = users.id) a on a.id = applications.user_id where job_id = %s and employee_id IS NOT NULL 
    order by skill_ct desc''', (job_id,))
    employee_applicants = list(db_obj.cursor.fetchall())
    db_obj.cursor.execute('''Select *, ifnull(a.skill_ct,0) from applications left join (select *, ifnull(s.skill_ct,0) from users left join (select count(*) as skill_ct, user_id from user_skills group by user_id) s on s.user_id = users.id) a on a.id = applications.user_id where job_id = %s and employee_id IS NULL 
    order by skill_ct desc''', (job_id,))
    non_employee_applicants = list(db_obj.cursor.fetchall())
    applicants = employee_applicants + non_employee_applicants
    return applicants

# update status of a user's application
def updateApplication(db_obj, app_id, status):
    db_obj.cursor.execute('''UPDATE applications set status = %s where application_id = %s''', (status, app_id))
    db_obj.db.commit()