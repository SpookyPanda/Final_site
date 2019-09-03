from django.urls import re_path, path

from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'posts'
#everythin here is under the pattern posts/
urlpatterns = [
	path('',
		views.PostList.as_view(),
		name='all'),
	path('new/',
		views.CreatePost.as_view(),
		name='create'),
	re_path(r'by/(?P<username>[-\w]+)/$',
		views.UserPosts.as_view(),
		name='for_user'),
	re_path(r'by/(?P<username>[-\w]+)/(?P<pk>\d+)/$',
		views.PostDetails.as_view(),
		name='single'),
	re_path(r'delete/(?P<pk>\d+)/$',
		views.DeletePost.as_view(), name='delete'),
	re_path(r'^(?P<pk>\d+)/comment/$',
		views.add_comment,
		name='add_comment'),
    re_path(r'^(?P<pk>\d+)/delete/$',
    	views.comment_delete,
    	name='delete_comment'),
]
# urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)