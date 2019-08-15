from django.db import models
from django.contrib import auth

#Users will be called with an @ (like twitter)
class User(auth.models.User,auth.models.PermissionsMixin):

	def __str__(self):
		return "@{}".format(self.username)
