from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from django.contrib.auth.models import User

from ..models import Asset
from .serializers import EntrySerializer, EntryLikesSerializer
from .permissions import IsOwnerOrReadOnly


class EntryListView(ListCreateAPIView):
    '''
    List of all assets
    '''

    queryset = Asset.objects.not_null()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'


class EntryReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_field = 'id'


class EntryLikesCreateView(APIView):
    '''
    API to post like if is there is no likes from user for this particular asset(201) and to delete it
    if there was any(204).
    '''

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        id = self.kwargs.get('id')
        return Asset.objects.filter(id=id)


    def get(self, request, format=None, *args, **kwargs):
        """
        Returns list of users liked asset
        :param request:
        :param format:
        :return:
        """
        id = self.kwargs.get('id')
        asset = Asset.objects.get(id=id)
        serializer = EntryLikesSerializer(asset)
        return Response(data=serializer.data)


    def post(self, request, format=None, *args, **kwargs):
        #TODO: Protect from liking by owner
        serializer = EntryLikesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # entry = Asset.objects.get(id = kwargs['id'])
        try:
            entry = Asset.objects.get(users_liked=request.user, id=kwargs['id'])
        except Asset.DoesNotExist:
            print('Failed')
            entry = None
        if entry:
            entry.users_liked.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            entry = Asset.objects.get(id=kwargs['id'])
            entry.users_liked.add(request.user)
            # serializer.save(users_liked = request.user, id = kwargs['id'])
            return Response(status=status.HTTP_201_CREATED)
