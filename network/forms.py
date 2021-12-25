
from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    """
    Form for creating comments (based on Comment model)
    fields:
    * content - comment's inner text
    """

    content = forms.CharField(widget=forms.Textarea(attrs={
                                    'placeholder': "Write a comment...",
                                    'rows': '1',
                                    'class': 'form-control',
                                    'aria-label': "comment content"
                             }))

    class Meta:
        model = Comment
        fields = ["content"]