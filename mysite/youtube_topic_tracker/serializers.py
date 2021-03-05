from rest_framework import serializers
from youtube_topic_tracker.models import YoutubeVideo
from django.contrib.auth.models import User, Group


class YoutubeVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YoutubeVideo
        fields = ['video_id', 'title', 'description', 'published_at', 'thumbnails']
