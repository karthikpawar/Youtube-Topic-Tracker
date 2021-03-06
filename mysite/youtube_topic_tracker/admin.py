from django.contrib import admin
from .models import CronLog, YoutubeVideo
# Register your models here.


class CronLogAdmin(admin.ModelAdmin):
    def field_ended_at(self, obj):
        return obj.ended_at.strftime("%d %b %Y %H:%M:%S")

    def field_started_at(self, obj):
        return obj.started_at.strftime("%d %b %Y %H:%M:%S")

    list_display = ['name', 'status', 'field_ended_at', 'field_started_at']


admin.site.register(CronLog, CronLogAdmin)


class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ['video_id', 'title', 'published_at', 'created_at', 'updated_at']
    list_filter = ['published_at']
    search_fields = ['title', 'description']


admin.site.register(YoutubeVideo, YoutubeVideoAdmin)
