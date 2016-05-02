from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response

from ..models import Entry,EntryLikes
from .serializers import EntrySerializer, EntryLikesSerializer
from .permissions import IsOwnerOrReadOnly



class EntryCreateReadView(ListCreateAPIView):
    '''
    List of all assets and endpoint for creating assets.
    '''

    queryset = Entry.objects.not_null()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

class EntryReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_field = 'id'


class EntryLikesCreateView(CreateAPIView):
    '''
    API to post like if is there is no likes from user for this particular asset(201) and to delete it
    if there was any(204).
    '''

    #TODO: return ammount of likes, asset owner cant like his asset, refactor model to have one to many relation

    queryset = EntryLikes.objects.all()
    serializer_class = EntryLikesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):#TODO: Move to perform_create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entry = Entry.objects.get(id = kwargs['id'])
        queryset=EntryLikes.objects.filter(user=request.user, entry = kwargs['id'])

        if queryset.exists():
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer.save(user = request.user, entry = entry)
            return Response(status=status.HTTP_201_CREATED)