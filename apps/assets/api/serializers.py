from rest_framework import serializers

from django.contrib.auth.models import User

from ..models import Entry, Category

#TODO: move to Users app
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    #descendants = serializers.CharField(read_only=True, source='get_descendants')
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')

class EntrySerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # category = serializers.IntegerField(source='category')
    user = UserSerializer(read_only=True)
    category = CategorySerializer()
    entry_type = serializers.CharField(source='get_entry_type_display')
    total_likes=serializers.ReadOnlyField(source='assets_liked__count')
    #last_update=serializers.ReadOnlyField(source='versionhistory__timestamp__max')
    # total_likes = serializers.ReadOnlyField()
    class Meta:
        model = Entry
        fields = (
        'id', 'category', 'name', 'description', 'languages', 'frameworks', 'repository', 'site', 'license', 'entry_type',
        'github_releases', 'changelog', 'locked', 'total_likes', 'user')

class EntryLikesSerializer(serializers.ModelSerializer):
    users_liked = serializers.PrimaryKeyRelatedField(many=True, queryset=Entry.objects.all(), required=False)
    class Meta:
        model = Entry
        fields = ('id', 'users_liked',)
        read_only_fields = ('id', 'users_liked')