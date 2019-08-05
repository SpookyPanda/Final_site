from django.db import models
from django.urls import reverse
from django.conf import settings

import misaka

from groups.models import Group

from django.contrib.auth import get_user_model

import os
# Create your models here.
User=get_user_model()

def get_image_path(instance, filename):
	ext = filename.split('.')[-1]
	filename =  "%s.%s"%(instance.id,ext)
	return os.path.join('media','photos',str(instance.user.username),filename)


class Post(models.Model):
	user = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now=True)
	message = models.TextField()
	message_html = models.TextField(editable=False)
	image = models.ImageField(upload_to=get_image_path, blank=True)
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
		