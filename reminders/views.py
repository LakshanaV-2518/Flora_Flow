from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import threading
from .forms import ReminderForm

# Function to send email
def send_email(sender_email, sender_password, recipient_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error: {e}")

# Create a thread to run the scheduler
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Django view to handle reminder setting
def set_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save()
            reminder_time = request.POST.get('reminder_time')
            email = request.POST.get('email')
            plant_collection = request.POST.getlist('plants')
            reminder_time = datetime.strptime(reminder_time, '%Y-%m-%dT%H:%M')

            def schedule_email():
                send_email(
                    sender_email="samplemail0403@gmail.com",
                    sender_password="vfee xday umoa fvqy",
                    recipient_email=email,
                    subject="Plant Watering Reminder",
                    message=f"Reminder to water your plants:\n\n{plant_collection}"
                )
                schedule_time = (datetime.now() + timedelta(hours=24)).strftime("%H:%M")
                schedule.every().day.at(schedule_time).do(schedule_email)

            schedule.every().day.at(reminder_time.strftime("%H:%M")).do(schedule_email)
            threading.Thread(target=run_schedule, daemon=True).start()

            return JsonResponse({"success": True, "message": "Reminder set successfully and emails will be sent at the scheduled time"})
    else:
        form = ReminderForm()

    return render(request, 'set_reminder.html', {'form': form})
