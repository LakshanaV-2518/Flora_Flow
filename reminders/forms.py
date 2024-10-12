from django import forms
from .models import PlantReminder
class ReminderForm(forms.ModelForm):
    class Meta:
        model = PlantReminder
        fields = ['email', 'plants', 'reminder_time']
