from django.db import models
class PlantEvent(models.Model):
    name = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name