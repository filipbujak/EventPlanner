from django.contrib import admin

from .models import Comment, Event, Vote


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "time", "place", "status")
    list_filter = ("status", "time")
    search_fields = ("title", "description", "place")
    date_hierarchy = "time"
    filter_horizontal = ("participants",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("event", "author", "created_at")
    list_filter = ("created_at",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("event", "author", "created_at")
    list_filter = ("created_at",)