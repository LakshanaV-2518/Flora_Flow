from django import forms
from .models import Post
from django.db import models


class PostForm(forms.ModelForm):
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        model = Post
        fields = ["title", "content"]
