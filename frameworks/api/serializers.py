from rest_framework import serializers

from ..models import Framework
from languages.api.serializers import LanguageSerializer


class FrameworkSerializer(serializers.ModelSerializer):#add site uri
    user = serializers.ReadOnlyField(source='user.username')
    languages = LanguageSerializer(many=True)
    #total_likes = serializers.ReadOnlyField(source='likes__count')
    class Meta:
        model = Framework
        fields = ['id', 'title', 'description', 'user','is_2d', 'is_3d', 'site', 'repository_url', 'languages',
                  'target_platforms', 'editor_platforms']
