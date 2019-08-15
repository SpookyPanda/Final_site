from django.urls import path, re_path
from . import views

app_name = 'groups'

#EVERY link in here is child of the address post/
urlpatterns = [
	#self explanatory links
	path("", views.ListGroups.as_view(), name='all'),
	path("new/",views.CreateGroup.as_view(), name='create'),
	#generates a link for each post with the group name
	re_path(r"^posts/in/(?P<slug>[-\w]+)/$", views.SingleGroup.as_view(), name='single'),
	#leave or join the group
	re_path(r"join/(?P<slug>[-\w]+)/$", views.JoinGroup.as_view(),name='join'),
	re_path(r"leave/(?P<slug>[-\w]+)/$",views.LeaveGroup.as_view(),name='leave'),
]