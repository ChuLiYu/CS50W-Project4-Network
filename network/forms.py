from django import forms
from .models import Like, Post, Following


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["creator", "like"]
        labels = {"context": ""}


class LikeUnlikeForm(forms.ModelForm):
    class Meta:
        model = Like
        exclude = ["creator", "post"]


class FollowForm(forms.ModelForm):
    class Meta:
        model = Following
        exclude = ["follower", "followee"]


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["context"]
