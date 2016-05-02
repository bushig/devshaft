from rest_framework import serializers

from ..models import Entry, EntryLikes, Category


class EntrySerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # category = serializers.IntegerField(source='category')
    user = serializers.ReadOnlyField(source='user.username')
    # category = serializers.CharField(source='category')
    total_likes=serializers.ReadOnlyField(source='entrylikes__count')
    last_update=serializers.ReadOnlyField(source='versionhistory__timestamp__max')
    # total_likes = serializers.ReadOnlyField()
    class Meta:
        model = Entry
        fields = ('id', 'category', 'user', 'name', 'description', 'total_likes', 'last_update')

class EntryLikesSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    # entry = serializers.DjangoModelField()
    class Meta:
        model = EntryLikes
        fields = ('user', 'entry')
        read_only_fields = ('user', 'entry')