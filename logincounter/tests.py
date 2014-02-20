from django.test import TestCase
from logincounter.models import UsersModels

# Create your tests here.

class UsersModelsTests(TestCase):
	"""
	Unittests for the Users model class.
	"""
	def setUp(self):
		UsersModels.objects.create(username="init_test", password="p", counter=1) 

	#1
	def testAdd1(self):
		"""
		Tests that adding a user works
		"""
		user_test1 = UsersModels.objects.get(username="init_test")
		self.assertEqual(user_test1.counter, 1)

	#2
	def testAddExists(self):
		"""
		Tests that adding a duplicate user name fails. 
		Should output ERR_USER_EXISTS = -2
		"""
		user_test2 = UsersModels().add("init_test", "p2")
		self.assertEqual(user_test2, -2)

	#3
	def testAdd2(self):
		"""
		Tests that adding 2 users works.
		The returned value should be 1.
		"""
		user1 = UsersModels().add("u1", "pass1")
		user2 = UsersModels().add("u2", "pass2")
		self.assertEqual(user1, 1)
		self.assertEqual(user2, 1)

	#4
	def testAdd_Empty(self):
		"""
		Tests that adding an user with empty username fails.
		self.ERR_BAD_USERNAME = -3
		"""
		empty_user = UsersModels().add("" , "")
		assert empty_user == -3

	#5
	def testAdd_EmptyUser(self):
		"""
		Tests that adding an user with empty username w/ passwordfails.
		self.ERR_BAD_CREDENTIALS = -1
		"""
		empty_user = UsersModels().add("" , "no_one")
		self.assertEqual(empty_user, -3)

	#6
	def test_login_wrong_passward(self):
		"""
		Test to make sure that the wrong password will give
		a self.ERR_BAD_CREDENTIALS = -1
		"""
		UsersModels().add("correct_login", "wrong_password")
		user3 = UsersModels().login("correct_login", "wrong_p")
		self.assertEqual(user3, -1)

	#7
	def test_login_wrong_login(self):
		"""
		Test to make sure that the wrong password will give
		a self.ERR_BAD_CREDENTIALS = -1
		"""
		user3 = UsersModels().login("correct_l", "wrong_password")
		self.assertEqual(user3, -1)

	#8
	def test_counter(self):
		"""
		Test to make sure that the counter is incrementing for each login.
		"""
		returning_user = UsersModels.objects.get(username="init_test")
		self.assertEqual(returning_user.counter, 1)
		UsersModels().login("init_test", "p")
		UsersModels().login("init_test", "p")
		returning_user = UsersModels.objects.get(username="init_test")
		self.assertEqual(returning_user.counter, 3)

	#9
	def test_long_password(self):
		"""
		Test to make sure that an error message will occur for long passwords
		self.ERR_BAD_PASSWORD = -4
		"""
		pass_long = UsersModels().add("normal", "sorry"*150)
		self.assertEqual(pass_long, -4)

	#10
	def test_long_username(self):
		"""
		Test to make sure that an error message will occur for long usernames
		ERR_BAD_USERNAME = -3
		"""
		user_long = UsersModels().add("norm"*150, "sorry")
		self.assertEqual(user_long, -3)

	#11
	def test_resetFixture(self):
		"""
		Test this function's success on call.
		No more users should be present for login. 
		ERR_BAD_CREDENTIALS = -1

		"""
		reset = UsersModels().TESTAPI_resetFixture()
		self.assertEqual(reset, 1)
		user_left = UsersModels().login("init_test", "p")
		self.assertEqual(user_left, -1)
