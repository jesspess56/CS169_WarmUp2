from django.db import models

# Create your models here.
class UsersModels(models.Model):
	username = models.CharField(max_length=128)
	password = models.CharField(max_length=128)
	counter = models.PositiveIntegerField()

 	#The success return code.
 	SUCCESS = 1

  	#Cannot find the user/password pair in the database (for login only)
	ERR_BAD_CREDENTIALS = -1
 
  	#trying to add a user that already exists (for add only)
	ERR_USER_EXISTS = -2

  	#invalid user name (empty or longer than MAX_USERNAME_LENGTH) (for add only)
	ERR_BAD_USERNAME = -3

 	#invalid password name (longer than MAX_PASSWORD_LENGTH) (for add only)
	ERR_BAD_PASSWORD = -4

 	#The maximum length of user name.
	MAX_USERNAME_LENGTH = 128

  	#The maximum length of the passwords.
	MAX_PASSWORD_LENGTH = 128


 	# Tells Python how to display the "unicode" representation of an object
 	def __unicode__(self):
 		return self.user


	def login(self,user,password):
		"""
		This function checks the user/password in the database.
		The comparison is case sensitive.
		On success, the function updates the count of logins in the database.
		On success the result is the count of logins (including this one) (>= 1)
		On failure the result is an error code (< 0) from the list below
			ERR_BAD_CREDENTIALS
		"""
		try:
			check_user = UsersModels.objects.get(username=user, password=password)
			check_user.counter += 1
			check_user.save()
			return check_user.counter
		except UsersModels.DoesNotExist:
			return self.ERR_BAD_CREDENTIALS

	def add(self, user, password):
		"""
		This function checks that the user does not exists, the user name is not empty. 
		(the password may be empty).
		On success the function adds a row to the DB, with the count initialized to 1
		On success the result is the count of logins
		On failure the result is an error code (<0) from the list below
		ERR_BAD_USERNAME, ERR_BAD_PASSWORD, ERR_USER_EXISTS
		If both the username and the password are invalid, the ERR_BAD_USERNAME should be the error code.
		"""
		#Check if the user already exists
		if(UsersModels.objects.filter(username=user)):
			return self.ERR_USER_EXISTS

		#Check username and password length
		if(len(user) > self.MAX_USERNAME_LENGTH or not user):
			return self.ERR_BAD_USERNAME

		#if only the password is incorrect
		elif(len(password) > self.MAX_PASSWORD_LENGTH):
			return self.ERR_BAD_PASSWORD
		#Create and add the new User
		else:
			new_user = UsersModels.objects.create(username=user, password=password, counter=1)
			#new_user.save()
			return new_user.counter


	def TESTAPI_resetFixture(self):
		"""
		This function is used only for testing, and should clear the database of all rows.
		It should always return SUCCESS (1)
		Used for testing
		"""
		UsersModels.objects.all().delete()
		return self.SUCCESS
