from django	import forms
from .models import Comment

#Need to be logged to comment so no need to add more fields
class CommentForm(forms.ModelForm):

	class Meta():
		model = Comment
		fields = ('text',)