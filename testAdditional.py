from django.test import TestCase, Client
from django.utils import unittest
from logincounter.models import UsersModels
import json

client = Client()

# Create your tests here.

class FunctionalTests(TestCase):

	#1
	def testAdd1(self):
		"""
		Tests that adding a user works
		"""
		response = client.post('/users/add', json.dumps({'user':'test1', 'password':'pass'}), content_type="application/json")
		response = json.loads(response.content)
		self.assertEqual(response['errCode'], 1)
		self.assertEqual(response['count'],1)

	#2
	def testAddExists(self):
		"""
		Tests that adding a duplicate user name fails. 
		Should output ERR_USER_EXISTS = -2
		"""
		response = client.post('/users/add', json.dumps({'user':'test2', 'password':'pass'}), content_type="application/json")
		response = client.post('/users/add', json.dumps({'user':'test2', 'password':'pass'}), content_type="application/json")
		response = json.loads(response.content)
		self.assertEqual(response['errCode'], -2)

	#3
	def testAdd2(self):
		"""
		Tests that adding 2 users works.
		The returned value should be 1.
		"""
		response1 = client.post('/users/add', json.dumps({'user':'test3', 'password':'pass'}), content_type="application/json")
		response1 = json.loads(response1.content)
		response2 = client.post('/users/add', json.dumps({'user':'test4', 'password':'pass'}), content_type="application/json")
		response2 = json.loads(response2.content)
		self.assertEqual(response1['errCode'], 1)
		self.assertEqual(response1['count'],1)
		self.assertEqual(response2['errCode'], 1)
		self.assertEqual(response2['count'],1)

	#4
	def testAddEmptyUsername(self):
		"""
		Tests that adding an user with empty username fails.
		self.ERR_BAD_USERNAME = -3
		"""
		response3 = client.post('/users/add', json.dumps({'user':'', 'password':'pass'}), content_type="application/json")
		response3 = json.loads(response3.content)
		self.assertEqual(response3['errCode'], -3)

	#5
	def testAddEmpty(self):
		"""
		Tests that adding an user with empty username fails.
		self.ERR_BAD_USERNAME = -3
		"""
		response3 = client.post('/users/add', json.dumps({'user':'', 'password':''}), content_type="application/json")
		response3 = json.loads(response3.content)
		self.assertEqual(response3['errCode'], -3)

	#6
	def test_login_no_input(self):
		"""
		Test to make sure that the wrong login will give
		a self.ERR_BAD_CREDENTIALS = -1
		"""
		response3 = client.post('/users/login', json.dumps({'user':'', 'password':''}), content_type="application/json")
		response3 = json.loads(response3.content)
		self.assertEqual(response3['errCode'], -1)

	#7
	def test_login_wrong_password(self):
		"""
		Test to make sure that the wrong password will give
		a self.ERR_BAD_CREDENTIALS = -1
		"""
		response4 = client.post('/users/add', json.dumps({'user':'test5', 'password':'pass'}), content_type="application/json")
		response4 = client.post('/users/login', json.dumps({'user':'test5', 'password':'p'}), content_type="application/json")
		response4 = json.loads(response4.content)
		self.assertEqual(response4['errCode'], -1)

	#8
	def test_counter(self):
		"""
		Test to make sure that the counter is incrementing for each login.
		In this case from 1 to 3.
		"""
		response5 = client.post('/users/add',json.dumps({'user':'test6','password':'pass'}),content_type="application/json")
		response5 = json.loads(response5.content)        
		self.assertEqual(response5['errCode'], 1)
		self.assertEqual(response5['count'],1)
		response5 = client.post('/users/login',json.dumps({'user':'test6','password':'pass'}),content_type="application/json")
		response5 = client.post('/users/login',json.dumps({'user':'test6','password':'pass'}),content_type="application/json")
		response5 = json.loads(response5.content)       
		self.assertEqual(response5['errCode'],1)
		self.assertEqual(response5['count'], 3)

	#9
	def test_long_password(self):
		"""
		Test to make sure that an error message will occur for long passwords
		self.ERR_BAD_PASSWORD = -4
		"""
		response = client.post('/users/add',json.dumps({'user':'test7','password':'pass'*150}),content_type="application/json")
		response = json.loads(response.content)
		self.assertEqual(response['errCode'], -4)

	def test_long_username(self):
		"""
		Test to make sure that an error message will occur for long usernames
		ERR_BAD_USERNAME = -3
		"""
		response = client.post('/users/add',json.dumps({'user':'test7'*150,'password':'pass'}),content_type="application/json")
		response = json.loads(response.content)
		self.assertEqual(response['errCode'], -3)

	#11
	def test_resetFixture(self):
		"""
		Test this function's success on call.
		No more users should be present for login. 
		ERR_BAD_CREDENTIALS = -1

		"""
		response = client.post('/TESTAPI/resetFixture',json.dumps({}),content_type="application/json")
		response = json.loads(response.content)
		self.assertEqual(response['errCode'], 1)
		print "moving on"
		response = client.post('/users/login',json.dumps({'user':'test6','password':'pass'}),content_type="application/json")
		response = json.loads(response.content)
		self.assertEqual(response['errCode'], -1)










