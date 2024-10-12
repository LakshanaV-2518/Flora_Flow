# tasks.py
import os
import logging
from celery import shared_task
from django.core.mail import send_mail

# Load environment variables if needed
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logger = logging.getLogger('reminders')

@shared_task
def send_reminder_email(email, plants):
    subject = "Plant Watering Reminder"
    message = f"Hi, don't forget to water your plants: {plants}."
    from_email = os.getenv('DEFAULT_FROM_EMAIL')  # Ensure this is set in your .env file
    
    try:
        send_mail(subject, message, from_email, [email])
        logger.info(f'Email sent successfully to {email}.')
    except Exception as e:
        logger.error(f'Error sending email to {email}: {e}')
