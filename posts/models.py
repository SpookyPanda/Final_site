from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.utils import timezone

import misaka

from groups.models import Group

import os
import uuid


User=get_user_model()


#Function to store uploaded images in /media/photos as the id of the post
#No image resize since it's a small site "_post.html" makes sure it fits on screen
def get_image_path(instance, filename):
	ext = filename.split('.')[-1]
	filename =  "%s.%s"%(instance.id,ext)
	return os.path.join('photos',str(instance.user.username),filename)

#Since it has not id when the form is filled it generates NONE.ext
class Post(models.Model):
	user = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now=True)
	message = models.TextField()
	message_html = models.TextField(editable=False)
	image = models.ImageField(upload_to=get_image_path,
		validators=[FileExtensionValidator(['jpg','png','jpeg','pdf','gif','ico','img'])],
		blank=True)
	group = models.ForeignKey(Group,related_name='posts',null=True,blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.message

	def save(self,*args,**kwargs):
		self.message_html = misaka.html(self.message)
		super().save(*args,**kwargs)

	def get_absolute_url(self):
		return reverse('posts:single', kwargs={'username':self.user.username,
												'pk':self.pk})

	class Meta:
		ordering = ['-created_at']
		unique_together = ['user','message']
		

class Comment(models.Model):
	user = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE, default=True)
	post = models.ForeignKey('posts.Post', related_name = 'comments', on_delete=models.CASCADE)
	text = models.TextField()
	create_date = models.DateTimeField(default=timezone.now)

	def get_absolute_url(self):
		return reverse("posts:single")

	def __str__(self):
		return self.text

#################
#working on this#
#################
# the idea is to make something like a like or upvote that actually works but not show a count
# i need to ellaborate the idea

class PostPoint(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	total = models.IntegerField()

	def __str__(self):
		pass

	class Meta():
		unique_together = ("user","post","total")


class CommentPoint(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
	total = models.IntegerField()

	def __str__(self):
		pass

	class Meta():
		unique_together = ("user","comment","total")