from django.db import models
from .validators import validate_file_extension

class Login(models.Model):
    email = models.CharField(max_length=64, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=32)

    class Meta:
        db_table = 'login'

class Companies(models.Model):
    company_id = models.CharField(primary_key=True, max_length=32)
    company_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'companies'


class Recruiters(models.Model):
    recruiter_id = models.CharField(primary_key=True, max_length=32)
    company = models.ForeignKey(Companies, models.DO_NOTHING)

    class Meta:
        db_table = 'recruiters'


class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    email = models.CharField(max_length=64)
    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    phone_number = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    employee_id = models.CharField(max_length=32, blank=True, null=True)
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True)
    recruiter = models.ForeignKey(Recruiters, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'users'

class Applications(models.Model):
    application_id = models.CharField(primary_key=True, max_length=32)
    job = models.ForeignKey('Jobpost', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    gender = models.CharField(max_length=1)
    resume_string = models.CharField(max_length=4000)
    phone_number = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'applications'

class Jobpost(models.Model):
    job_id = models.CharField(primary_key=True, max_length=64)
    job_name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    company = models.ForeignKey(Companies, models.DO_NOTHING)
    company_name = models.CharField(max_length=64)
    pay = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    post_date = models.DateField()
    due_date = models.DateField()
    recruiter = models.ForeignKey('Recruiters', models.DO_NOTHING)
    description = models.CharField(max_length=2500)

    class Meta:
        managed = False
        db_table = 'jobpost'

class Resume(models.Model):
    filename = models.CharField(max_length=100)
    doc = models.FileField(upload_to='resumes/docx/')

    def _str_(self):
        return self.filename