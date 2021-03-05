from django.db import models
from jsonfield import JSONField
import datetime
from django.utils import timezone


class CronLog(models.Model):

    choices_for_status = (
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
        ('running', 'Running'),
        ('idle', 'idle'),)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, default=choices_for_status[1][0], choices=choices_for_status)
    error_log = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True, db_index=True)
    ended_at = models.DateTimeField(auto_now=True, db_index=True)


class YoutubeVideo(models.Model):
    video_id = models.CharField(max_length=255, unique=True)
    etag = models.CharField(max_length=255, unique=True)
    title = models.TextField()
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnails = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video_id
