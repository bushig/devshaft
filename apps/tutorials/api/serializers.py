from rest_framework import serializers

from apps.languages.api.serializers import LanguageSerializer
from apps.frameworks.api.serializers import FrameworkShortSerializer
from ..models import Tutorial


# class TutorialSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     languages = LanguageSerializer(many=True)
#
#     # total_likes = serializers.ReadOnlyField(source='likes__count')
#     class Meta:
#         model = Tutorial
#         fields = ['id', 'title', 'description', 'user', 'is_2d', 'is_3d', 'site', 'repository_url', 'languages',
#                   'target_platforms', 'editor_platforms']


class TutorialLikesSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, queryset=Tutorial.objects.all(), required=False, source='users_liked')

    class Meta:
        model = Tutorial
        fields = ('id', 'likes',)
        read_only_fields = ('id', 'likes')
