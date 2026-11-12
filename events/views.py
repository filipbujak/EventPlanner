from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EventForm
from .models import Event


def home(request):
    """Lista wydarzeń z filtrem czasu (?when=upcoming/past/all) i wyszukiwarką (?q=)."""
    events = Event.objects.select_related("author")
    now = timezone.now()

    when = request.GET.get("when", "upcoming")
    if when == "past":
        events = events.filter(time__lt=now).order_by("-time")
    elif when != "all":
        when = "upcoming"
        events = events.filter(time__gte=now)

    q = request.GET.get("q", "").strip()
    if q:
        events = events.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(place__icontains=q)
        )

    page_obj = Paginator(events, 10).get_page(request.GET.get("page"))
    return render(request, "events/home.html", {"page_obj": page_obj, "when": when, "q": q})


def event_detail(request, pk):
    event = get_object_or_404(Event.objects.select_related("author"), pk=pk)
    return render(request, "events/event_detail.html", {
        "event": event,
        "can_edit": event.can_edit(request.user),
    })


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            messages.success(request, "Wydarzenie zostało utworzone.")
            return redirect(event)
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.can_edit(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Zmiany zostały zapisane.")
            return redirect(event)
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_form.html", {"form": form, "event": event})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.can_edit(request.user):
        raise PermissionDenied

    if request.method == "POST":
        if event.photo:
            event.photo.delete(save=False)  # usuwa też plik zdjęcia z dysku
        event.delete()
        messages.success(request, f"Usunięto wydarzenie „{event.title}”.")
        return redirect("home")
    return render(request, "events/event_confirm_delete.html", {"event": event})