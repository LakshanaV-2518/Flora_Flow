from django.shortcuts import render, redirect
from django.http import HttpResponse
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
        # Create the MIMEMultipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message body
        msg.attach(MIMEText(message, 'plain'))

        # Create the SMTP session for Gmail and login
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(msg)
        print(f"Email sent successfully to {recipient_email}")

        # Close the server connection
        server.quit()

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
        form = ReminderForm(request.POST)  # Use your ReminderForm
        if form.is_valid():
            # Save the reminder to the database
            reminder = form.save()  # Save the reminder

            # Extract data for scheduling
            reminder_time = request.POST.get('reminder_time')
            email = request.POST.get('email')
            plant_collection = request.POST.getlist('plants')

            # Convert reminder_time to the correct format
            reminder_time = datetime.strptime(reminder_time, '%Y-%m-%dT%H:%M')

            # Function to schedule email every 2 hours starting from reminder_time
            def schedule_email():
                send_email(
                    sender_email="samplemail0403@gmail.com",
                    sender_password="vfee xday umoa fvqy",
                    recipient_email=email,
                    subject="Plant Watering Reminder",
                    message=f"Reminder to water your plants:\n\n{plant_collection}"
                )
                # Reschedule to run after 2 hours
                schedule_time = (datetime.now() + timedelta(hours=24)).strftime("%H:%M")
                schedule.every().day.at(schedule_time).do(schedule_email)

            # Schedule the first email at the reminder_time
            schedule.every().day.at(reminder_time.strftime("%H:%M")).do(schedule_email)

            # Start a background thread for scheduling
            threading.Thread(target=run_schedule, daemon=True).start()

            return HttpResponse("Reminder set successfully and emails scheduled every 2 hours!")
    else:
        form = ReminderForm()

    return render(request, 'set_reminder.html', {'form': form})
