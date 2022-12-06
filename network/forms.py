from django import forms
from .models import Like, Post, Following


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["creator", "like"]


class LikeUnlikeForm(forms.ModelForm):
    class Meta:
        model = Like
        exclude = ["creator", "post"]
