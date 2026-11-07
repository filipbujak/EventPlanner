from django.shortcuts import render

from .models import Event


def home(request):
    events = Event.objects.select_related("author")
    return render(request, "events/home.html", {"events": events})