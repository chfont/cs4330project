from django.urls import path
from . import views
urlpatterns = [
	path('', views.login, name='login'),
	path('login', views.login, name='login'),
	path('register', views.register, name='register'),
	path('home', views.profile, name='profile'),
	path('jobsearch', views.jobsearch, name='jobsearch'),
	path('jobpost', views.jobpost, name='jobpost')
]
