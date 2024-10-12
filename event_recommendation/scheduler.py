from apscheduler.schedulers.background import BackgroundScheduler
from .scraping_script import scrape_and_update_events

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_and_update_events, 'interval', hours=24)  # Run every 24 hours
    scheduler.start()