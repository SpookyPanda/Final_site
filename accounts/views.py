from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms

#Nothing but the creation form
class SignUp(CreateView):
	form_class = forms.UserForm
	success_url = reverse_lazy('login')
	template_name = 'accounts/signup.html'
