from django.shortcuts import render
from django.views.generic import TemplateView


#class Home(TemplateView):
#    template_name = ''

def upload(uploaded_file):
    print(uploaded_file.name)
    print(uploaded_file.size)
    return True