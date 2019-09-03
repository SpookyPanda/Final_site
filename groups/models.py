from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import template

from django.utils.text import slugify
import misaka

# Create your models here.

#User var to call the main model, saves code in class
User = get_user_model()
#self explanatory, register the template
register = template.Library()


class Group(models.Model):
	#It works more as a tag than anything, the posts logic is in posts/Post
	#An user can like a group like reddit or fb and see content posted there

	name=models.CharField(max_length=200, unique=True)
	slug=models.SlugField(allow_unicode=True, unique=True)
	description = models.TextField(blank=True,default='')
	description_html = models.TextField(editable=False,default='',blank=True)
	members = models.ManyToManyField(User,through='GroupMember')

	def __str__(self):
		return self.name

	def save(self,*args,**kwargs):
		self.slug = slugify(self.name)
		self.description_html = misaka.html(self.description)
		super().save(*args,**kwargs)

	def get_absolute_url(self):
		return reverse('groups:single',kwargs={'slug':self.slug})

	class Meta:
		ordering=['name']

class GroupMember(models.Model):
	#This registers the user in the group, it doesn't do much
	#just bump a +1 in the  group member count
	#the info is stored in the user too if you want to use it
	group = models.ForeignKey(Group,related_name='suscription',on_delete=models.CASCADE)
	user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username



