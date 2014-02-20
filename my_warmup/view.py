from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render

def login_page(request):
	return render(request, 'main_screen.html')

