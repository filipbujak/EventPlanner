from django.db import models
from django.conf import settings

class Event(models.Model):
    STATUS_CHOICES = [
        ('propozycje', 'Propozycja'),
        ('zaakceptowane', 'Zaakceptowane'),
        ('anulowane', 'Anulowane'),
    ]

    title = models.CharField(max_length=200, verbose_name="Tytuł wydarzenia")
    description = models.TextField(max_length=67000, verbose_name="Opis")
    photo = models.ImageField(upload_to="events/", blank=True, null=True, verbose_name="Zdjęcie/Plakat")
    time = models.DateTimeField(verbose_name="Data i godzina rozpoczęcia")
    place = models.CharField(max_length=60, verbose_name="Miejsce")
    
    # Autor wydarzenia
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="created_events",
        verbose_name="Autor"
    )
    
    # Uczestnicy wydarzenia
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="joined_events", 
        blank=True,
        verbose_name="Uczestnicy"
    )
    
    # Flaga do powiadomień mailowych 
    reminder_sent = models.BooleanField(default=False, verbose_name="Czy wysłano przypomnienie")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='propozycje', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"
        ordering = ['time']


class Vote(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="votes", verbose_name="Wydarzenie")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Użytkownik")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data głosu")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "author"], name="one_vote_per_user")
        ]
        verbose_name = "Głos"
        verbose_name_plural = "Głosy"

    def __str__(self):
        return f"Głos {self.author} na {self.event.title}"


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments", verbose_name="Wydarzenie")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Autor komentarza")
    description = models.TextField(max_length=1000, verbose_name="Treść komentarza")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    class Meta:
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"
        ordering = ['created_at']

    def __str__(self):
        return f"Komentarz od {self.author} do {self.event.title}"