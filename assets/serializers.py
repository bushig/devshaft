from rest_framework import serializers

from .models import Entry, EntryLikes


class EntrySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    # total_likes = serializers.ReadOnlyField()
    class Meta:
        model = Entry
        fields = ('id', 'category', 'user', 'name', 'description', 'total_likes')

class EntryLikesSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    # entry = serializers.DjangoModelField()
    class Meta:
        model = EntryLikes
        fields = ('user', 'entry')
        read_only_fields = ('user', 'entry')