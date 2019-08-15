from django.views.generic import TemplateView

#Views for the main pages

class ThanksPage(TemplateView):
	#Page shown when you log out
	template_name = "thanks.html"

class TestPage(TemplateView):
	#Page after succesful log in
	template_name = "test.html"

class HomePage(TemplateView):
	#Main page
	template_name = "index.html"