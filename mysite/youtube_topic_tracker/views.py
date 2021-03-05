from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from youtube_topic_tracker.serializers import YoutubeVideoSerializer
from youtube_topic_tracker.models import YoutubeVideo
from django.conf import settings
from rest_framework import filters


class YoutubeVideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view latest youtube videos.
    """
    queryset = YoutubeVideo.objects.all().order_by('-published_at')
    serializer_class = YoutubeVideoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['published_at']
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
