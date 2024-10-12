import requests
from bs4 import BeautifulSoup
from .models import PlantEvent

def scrape_and_update_events():
    url = 'https://10times.com/india/horti-flora'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming you are using a class 'event-card', adjust as per actual HTML structure
    event_cards = soup.find_all('div', class_='event-card')  # Replace with actual tag and class

    events = []  # List to hold event data

    for card in event_cards:
        event_name = card.find('h2').text.strip()  # Adjust tag according to the HTML structure
        event_date = card.find('div', class_='date').text.strip()
        event_location = card.find('div', class_='location').text.strip()
        event_url = card.find('a', href=True)['href']

        # Collect event data for debugging
        event_data = {
            'name': event_name,
            'date': event_date,
            'location': event_location,
            'url': event_url
        }
        events.append(event_data)

         # Save each event to the database
    for event in events:
        PlantEvent.objects.update_or_create(
            name=event['name'],
            defaults={'date': event['date'], 'location': event['location'], 'url': event['url']}
        )

    print("Events saved to the database.")

    # Print the events to debug scraping
    print(events)

    # Check if scraping returned any events
    if not events:
        print("No events found, check the website structure.")
