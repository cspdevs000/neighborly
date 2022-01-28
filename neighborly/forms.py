from django import forms
from neighborly.models import Post, Reply, Building, ExtendUser

class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Add a new post....'
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
            'placeholder': 'type reply here',
        })
    )
    class Meta:
        model = Reply
        fields = ['body']

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields= '__all__'

class ExtendBuildingForm(forms.ModelForm):
    class Meta:
        model = ExtendUser
        fields = ['building']
    def __init__(self, *args, **kwargs):
        super(ExtendBuildingForm, self).__init__(*args, **kwargs)
        self.fields['building'].required = False