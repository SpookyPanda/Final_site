from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.urls import reverse
from django.contrib.auth.mixins import (LoginRequiredMixin
										,PermissionRequiredMixin)
from django.views import generic
from .models import Group, GroupMember

#IF YOU CAN'T FIND THE URL:
#if the template name is not listed in the class
#it is generated and linked AUTOMATICALLY
#
#E.G.
#the html for ListGroups is group_list.html, no need to
#add it to URLS or specify the file 

class CreateGroup(LoginRequiredMixin,generic.CreateView):
	fields = ('name','description')
	model = Group

class SingleGroup(generic.DetailView):
	model = Group

class ListGroups(generic.ListView):
	model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

	def get_redirect_url(self,*args,**kwargs):
		return reverse("groups:single",kwargs={"slug":self.kwargs.get("slug")})

	def get(self,request,*args,**kwargs):
		group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

		try:
			GroupMember.objects.create(user=self.request.user, group=group)

		except IntegrityError:
			messages.warning(self.request("You are already a proud member of {}".format(group.name)))

		else:
			messages.success(self.request,"You are now a member in {}".format(group.name))

		return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

	def get_redirect_url(self,*args,**kwargs):
		return reverse("groups:single",kwargs={"slug":self.kwargs.get("slug")})

	def get(self,request,*args,**kwargs):

		try:
			membership = GroupMember.objects.filter(
				user=self.request.user,
				group__slug=self.kwargs.get("slug")
				).get()

		except GroupMember.DoesNotExist:
			messages.warning(self.request,"You are not in this group")

		else:
			membership.delete()
			messages.success(self.request, "you successfully left")
			return super().get(request,*args,**kwargs)