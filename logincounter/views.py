from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from logincounter.models import UsersModels
from my_warmup.view import login_page
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.

@csrf_exempt
def user_login(request):
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

			#responsde_data returns the count and is SUCCESS = 1
			else:
				data['errCode'] = 1
				data['count'] = response_data
				return HttpResponse(json.dumps(data), content_type = 'application/json')
	
		#handle catastrophic errors using status code 500
		else:
			return HttpResponseServerError("Post Data Issue in User_Login")
	else:
		return render(request, 'main_screen.html')

@csrf_exempt
def user_add(request):
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
		return render(request, 'main_screen.html')

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
		return render(request, 'main_screen.html')

@csrf_exempt
def call_unitTests(request):
	from logincounter.tests import UsersModelsTests
	import unittest
	from django.test.utils import setup_test_environment

	setup_test_environment()

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



	



