# Database queries are here, to remove clutter from views

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


def getJobApplicationsOfUser(db_obj, id):
    db_obj.cursor.execute("SELECT status, job_name, company_name FROM applications, jobpost where applications.user_id = %s and applications.job_id = jobpost.job_id", (id,))
    return db_obj.cursor.fetchall()

def getEmployeeInfo(db_obj, employee_id):
    db_obj.cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    return db_obj.cursor.fetchone()

def getJobPost(db_obj, job_id):
    db_obj.cursor.execute("select * from jobpost where job_id = %s", (job_id,))
    return db_obj.cursor.fetchone()

def getCompany(db_obj, company_name):
    db_obj.cursor.execute("SELECT * FROM companies WHERE company_name = %s", (company_name,))
    return db_obj.cursor.fetchone()

def isUniqueApplication(db_obj, user_id, job_id):
    db_obj.cursor.execute("select * from applications where job_id = %s and user_id = %s", (job_id, user_id))
    results = db_obj.cursor.fetchall()
    return len(results) == 0

def getApplicationCountByUser(db_obj, user_id):
    db_obj.cursor.execute("select count(*) from applications where user_id = %s", (user_id,))
    results = db_obj.cursor.fetchone()
    return results[0]

def addApplicationToTable(db_obj, app_id, job_id, user_id):
    db_obj.cursor.execute("insert into applications(application_id, job_id, user_id, status) values(%s, %s, %s, %s)", (app_id, job_id, user_id, 'SUBMITTED'))
    db_obj.db.commit()
    return True

def getJobPostsByRecruiter(db_obj, rec_id):
    db_obj.cursor.execute("select * from jobpost where recruiter_id = %s", (rec_id,))
    return db_obj.cursor.fetchall()