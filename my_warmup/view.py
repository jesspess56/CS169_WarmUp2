from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render

def home(request):
	return render(request, 'login_screen.html')
