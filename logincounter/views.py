from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, RequestContext
from logincounter.models import UsersModels
from logincounter.forms import LoginForm
from my_warmup.view import home
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
import json

# Create your views here.

#Determine if it's json or html
def is_json_request(request):
	if (request.META['CONTENT_TYPE'] == 'application/json'):
		return True
	else:
		return False

#For HTML texts
@csrf_exempt
def login_or_add(request):
	if request.method == "POST" and not is_json_request(request):
		method = request.POST
	elif request.method == "GET" and not is_json_request(request):
		method = request.GET
	else:
		raise Exception("Request is neither GET or PUT")

	#Dealing with login-button
	if "login_button" in method:
		form = LoginForm(method)
		#breaks if login input is empty
		if (form.is_valid()):
			cd = form.cleaned_data
			user = cd['username']
			password = cd['password']
			try:
				response_data = UsersModels().login(user, password)
				message = error_message(response_data)
				if (response_data == -1):
					return render(request, 'login_screen.html', {'error': True,'error_message': message})
			except ValueError:
				print "Invalid call to HTML"
			else:
				return render(request, 'logged_page.html', {'error': False, 'name': user,'number':response_data})
		else:
			message = error_message(-1)
			return render(request, 'login_screen.html', {'error': True,'error_message': message})
	
	#Dealing with add-button
	elif "add_user_button" in method:
		form = LoginForm(method)
		if form.is_valid():
			cd = form.cleaned_data
			user = cd['username']
			password = cd['password']
			try:
				response_data = UsersModels().add(user, password)
				message = error_message(response_data)
				if (response_data == 1):
					return render(request, 'logged_page.html', {'error': False, 'name': user, 'number':response_data })
				
			except ValueError:
				print "Invalid Add in HTML"
			else:
				return render(request, 'login_screen.html', {'error':True, 'error_message': message})
		else:
			message = error_message(-3)
			return render(request, 'login_screen.html', {'error': True, 'error_message': message})
	else:
		raise Exception("Login or Add was not selected")

@csrf_exempt
def users_login(request):
	if (is_json_request(request)):
		#Check to make sure it is a POST
		if (request.method == 'POST' and request.path =='/users/login'):
			content_type = request.META['CONTENT_TYPE']

			#Check to see if it's a JSON and convert to python dictionary
			if (content_type == 'application/json'):
				try:
					data = json.loads(request.body)
					user = data['user']
					password = data['password']
					#response_data will return either: ERR_BAD_CREDENTIALS = -1
					response_data = UsersModels().login(user, password)
					if (response_data == -1):
						data['errCode'] = -1 
						return HttpResponse(json.dumps(data), content_type = 'application/json')
				except ValueError:
					#decoding failed
					print "strange login"

				#response_data returns the count and is SUCCESS = 1
				else:
					data['errCode'] = 1
					data['count'] = response_data
					return HttpResponse(json.dumps(data), content_type = 'application/json')

			#handle catastrophic errors using status code 500
			else:
				return HttpResponseServerError("Post Data Issue in User_Login")
		else:

			return render(request, 'login_screen.html')

@csrf_exempt
def user_add(request):
	if (is_json_request(request)):
		#if its an add function then it will send information to the following
		if (request.method =="POST" and request.path=='/users/add'):
			content_type = request.META['CONTENT_TYPE'] #get_content_type(request)

			#Check to see if it's a JSON and convert to python dictionary
			if (content_type == 'application/json'):
				try:
					data = json.loads(request.body) 
					user = data['user']
					password = data['password']
					response_data = UsersModels().add(user, password)
					# ERR_USER_EXISTS = -2
					if (response_data == -2):
						data['errCode'] = -2
						return HttpResponse(json.dumps(data), content_type = 'application/json')

					# ERR_BAD_USERNAME = -3
					if (response_data == -3):
						data['errCode'] = -3
						return HttpResponse(json.dumps(data), content_type = 'application/json')
					
					# ERR_BAD_PASSWORD = -4
					if (response_data == -4):
						data['errCode'] = -4
						return HttpResponse(json.dumps(data), content_type = 'application/json')
					#responsd_data returns the count which is 1 and is SUCCESS = 1
				except ValueError:
					#decoding failed
					print "strange add"
				else:
					data['errCode'] = 1
					data['count'] = response_data
					return HttpResponse(json.dumps(data), content_type = 'application/json')
		
		#handle catastrophic errors using status code 500
			else:
				return HttpResponseServerError("Post Data Issue in User_Add")
		else:
			return render(request, 'login_screen.html')

def error_message(response_data):
	# success
	if (response_data == 1): return ""
	# ERR_BAD_CREDENTIALS = -1
	if (response_data == -1): return "Invalid username and password combination. Please try again."
	# ERR_USER_EXISTS = -2
	if (response_data == -2): return "This user name already exists. Please try again."
	# ERR_BAD_USERNAME = -3
	if (response_data == -3): return "The user name should be non-empty and at most 128 characters long. Please try again." 
	# ERR_BAD_PASSWORD = -4
	if (response_data == -4): return "The password should be at most 128 characters long. Please try again." 



@csrf_exempt
def call_resetFixture(request):
	if (request.method =="POST" and request.path=='/TESTAPI/resetFixture'):
		content_type = request.META['CONTENT_TYPE']

		if (content_type == 'application/json'):
			try:
				data = json.loads(request.body)
				data['errCode'] = UsersModels().TESTAPI_resetFixture()
			except ValueError:
				print "strange resetFix"
			return HttpResponse(json.dumps(data), content_type='application/json')
		else:
			return HttpResponseServerError("POST data issue in resetFixture")
	else:
		return render(request, 'login_screen.html')

@csrf_exempt
def call_unitTests(request):
	from logincounter.tests import UsersModelsTests
	import unittest

	if (request.method =="POST" and request.path=='/TESTAPI/unitTests'):
		content_type = get_content_type(request)
		response_data = {}

		if (content_type == 'application/json'):
			try:
				suite = unittest.TestLoader().loadTestsFromTestCase(UsersModelsTests)
				testing_results = unittest.TextTestRunner(verbosity=2).run(suite)
				response_data['nrFailed'] = len(testing_results.failures)
				response_Data['totalTests'] = testing_results.testRuns
				response_data['output'] = "{}{}".format('\n'.join([result[1] for result in test_results.errors]),'\n'.join([result[1] for result in testing_results.failures]))
			except Exception:
				response_data['nrFailed'] = 0
				response_data['output'] = "Error in running UnitTest"
				response_Data['totalTests'] = 0 
			return HttpResponse(json.dumps(response_data), content_type='application/json')
		else:
			return HttpResponseServerError("Requests invalid in unitTests")



	



