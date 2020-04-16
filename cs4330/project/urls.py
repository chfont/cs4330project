from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.login, name='login'),
	path('login', views.login, name='login'),
	path('register', views.register, name='register'),
	path('home', views.profile, name='profile'),
	path('jobsearch', views.jobsearch, name='jobsearch'),
	path('jobpost', views.jobpost, name='jobpost'),
	path('messages', views.messages, name='message'),
	path('apply', views.apply, name='apply'),
	path('view_posts', views.recruiter_post, name='view_posts'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

