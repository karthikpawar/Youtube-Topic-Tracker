from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'youtubevideos', views.YoutubeVideoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
