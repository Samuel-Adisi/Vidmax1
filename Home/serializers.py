from rest_framework import serializers
from.models import Video


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Video
        fields='__all__'


from .models import Videos

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ['id', 'title', 'author', 'thumbnail_image', 'video_file', 'duration', 'published_at']