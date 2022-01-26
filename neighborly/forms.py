from django import forms
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

class ReplyForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '1',
            'placeholder': 'type reply here'
        })
    )
    class Meta:
        model = Reply
        fields = ['body']