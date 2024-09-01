from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title



class Flower(models.Model):
    name = models.CharField(max_length=100)
    # image = models.ImageField(upload_to="flowers/")
    description = models.TextField()

    def __str__(self):
        return self.name


class CareTip(models.Model):
    flower = models.ForeignKey(
        Flower, related_name="care_tips", on_delete=models.CASCADE
    )
    tip = models.TextField()

    def __str__(self):
        return f"Care Tip for {self.flower.name}"
