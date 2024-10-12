from django.shortcuts import render
from .models import PlantEvent

def event_list(request):
    events = PlantEvent.objects.all()  # Fetch all events from the database
    return render(request, 'event_recommendation/event_list.html', {'events': events})

