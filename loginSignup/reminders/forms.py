from django import forms
from .models import PlantReminder

class PlantReminderForm(forms.ModelForm):
    class Meta:
        model = PlantReminder
        fields = ['email', 'plants', 'reminder_time']
