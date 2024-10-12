from django.db import models

class PlantReminder(models.Model):
    email = models.EmailField()
    plants = models.TextField()
    reminder_time = models.DateTimeField()
    
    def __str__(self):
        return self.email