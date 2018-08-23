from rest_framework import serializers

from ..models import Framework, Platform
from apps.languages.api.serializers import LanguageSerializer

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = "__all__"


class FrameworkSerializer(serializers.ModelSerializer):#add site uri
    user = serializers.ReadOnlyField(source='user.username')
    languages = LanguageSerializer(many=True)
    target_platforms = PlatformSerializer(many=True)
    editor_platforms = PlatformSerializer(many=True)

    #total_likes = serializers.ReadOnlyField(source='likes__count')
    class Meta:
        model = Framework
        fields = ['id', 'title', 'description', 'user', 'is_2d', 'is_3d', 'site', 'repository_url', 'languages',
                  'target_platforms', 'editor_platforms']

class FrameworkLikesSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, queryset=Framework.objects.all(), required=False)
    class Meta:
        model = Framework
        fields = ('id', 'likes',)
        read_only_fields = ('id', 'likes')