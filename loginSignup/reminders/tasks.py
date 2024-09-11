import logging
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_reminder_email(email,plants):
    logger = logging.getLogger(__name__)
    
    logger.info(f'Sending reminder email to {email} for plants:{plants}')
    plants_list =','.join(plants) if isinstance(plants,list) else plants
    breakpoint()
    try:
        send_mail(
            'Plant Reminder',
            'This is a reminder to take care of your plants.',
            'lakshanavivek2518@gmail.com',  # Update with your actual sender email
            [email],
            fail_silently=False,
        )
        logger.info('Email sent successfully.')
    except Exception as e:
        logger.error(f'Error sending email: {e}')


