from django import forms
from django.forms import ModelForm
from neighborly.models import Post, Reply

class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'type post here'
        })
    )
    class Meta:
        model = Post
        fields = ['body']
