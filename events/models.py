from django.db import models
from django.conf import settings
# Create your models here.
class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="events/", blank=True)
    description = models.TextField(max_length=67000)
    time = models.DateTimeField()
    place = models.CharField(max_length=60)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="joined_events", blank=True)
    reminder_sent = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
class Vote(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="votes")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["event", "author"], name="one_vote_per_user")]
class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
