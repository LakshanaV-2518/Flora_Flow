from django.shortcuts import render, redirect
from .forms import PlantReminderForm
from .models import PlantReminder
from .tasks import send_reminder_email
import logging
from celery import shared_task
from django.core.mail import send_mail 
import smtplib

logger = logging.getLogger('reminders')

@shared_task
def send_reminder_email(email, plants):
    # Your email sending logic here
    # Example:
    subject = "Plant Watering Reminder"
    message = f"Hi, don't forget to water your plants: {plants}."
    from_email = "noreply@yourdomain.com"
    
    send_mail(subject, message, from_email, [email])

def set_reminder(request):
    if request.method == 'POST':
        form = PlantReminderForm(request.POST)
        if form.is_valid():
            try:
                reminder = form.save()  # Save the data to the database

                # Schedule the email to be sent using Celery
                send_reminder_email.apply_async(
                    (reminder.email, reminder.plants),  # Pass both email and plants
                    eta=reminder.reminder_time
                )
                logger.info(f'Reminder set for {reminder.email} at {reminder.reminder_time}')
                return redirect('reminder_set')
            except Exception as e:
                logger.error(f'Error scheduling reminder for {reminder.email}: {e}')
                form.add_error(None, 'There was an error scheduling your reminder. Please try again.')
        else:
            logger.warning(f'Form is invalid: {form.errors}')
    else:
        form = PlantReminderForm()
    
    return render(request, 'set_reminder.html', {'form': form})

def reminder_set(request):
    return render(request, 'reminder_set.html')
