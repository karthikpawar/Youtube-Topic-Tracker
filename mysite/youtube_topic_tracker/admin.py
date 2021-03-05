from django.contrib import admin
from .models import CronLog, YoutubeVideo

# Register your models here.


class CronLogAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'started_at', 'ended_at']


admin.site.register(CronLog, CronLogAdmin)


class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ['video_id', 'title', 'published_at', 'created_at', 'updated_at']
    list_filter = ['published_at']
    search_fields = ['title', 'description']


admin.site.register(YoutubeVideo, YoutubeVideoAdmin)
