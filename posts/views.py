from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views import generic
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from braces.views import SelectRelatedMixin

from .models import Post

from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import CommentForm
from django.contrib.auth.decorators import login_required

#IF YOU CAN'T FIND THE URL:
#if the template name is not defined in the class
#it is generated and linked AUTOMATICALLY

User=get_user_model()

#############
#Posts stuff#
#############

class PostList(SelectRelatedMixin,generic.ListView):
	model = Post
	select_related = ('user','group')


class UserPosts(generic.ListView):
	model = Post
	template_name = 'posts/user_post_list.html'

	def get_queryset(self):
		try:
			self.post_user = User.objects.prefetch_related("posts").get(
					username__iexact = self.kwargs.get("username")
				)

		except ObjectDoesNotExist:
			raise Http404

		else:
			return self.post_user.posts.all()

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context["post_user"] = self.post_user
		return context


class PostDetails(SelectRelatedMixin,generic.DetailView):
	model = Post
	select_related = ('user', 'group')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user__username__iexact=self.kwargs.get("username"))


class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
	fields = ('message','group','image')
	model = Post

	def form_valid(self,form):
		self.object = form.save(commit=False)
		if 'image' in self.request.FILES:
			self.object.image = self.request.FILES['image']
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)


class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
	model = Post
	select_related = ('user','group')
	success_url = reverse_lazy("posts:all")

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user_id=self.request.user.id)

	def delete(self,*args,**kwargs):
		messages.success(self.request,"Post deleted")
		return super().delete(*args,**kwargs)

################
#Comments stuff#
################

@login_required
def add_comment(request,pk):
	post = get_object_or_404(Post,pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = comment.user.username
			comment.post = post
			comment.save()
			return redirect('posts:single',username=post.user.username,pk=post.pk)
	else:
		form = CommentForm()
	return render(request,'posts/comment_form.html',{'form':form})



@login_required
def comment_delete(request, pk):
	post = get_object_or_404(Comment,pk=pk)
	post_pk = comment.post.pk
	comment.delete()
	return redirect('post_details', pk=post_pk)