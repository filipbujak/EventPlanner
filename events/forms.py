from django import forms
from django.utils import timezone

from .models import Event

DATETIME_FORMAT = "%Y-%m-%dT%H:%M"


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "photo", "time", "place", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "time": forms.DateTimeInput(attrs={"type": "datetime-local"}, format=DATETIME_FORMAT),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["time"].input_formats = [DATETIME_FORMAT]
        # Nowe wydarzenie zawsze startuje jako "Propozycja" - status zmienia się dopiero przy edycji
        if self.instance.pk is None:
            del self.fields["status"]

    def clean_time(self):
        time = self.cleaned_data["time"]
        if self.instance.pk is None and time < timezone.now():
            raise forms.ValidationError("Nie można utworzyć wydarzenia w przeszłości.")
        return time