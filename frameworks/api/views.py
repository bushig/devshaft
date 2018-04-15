from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import permissions, status


from ..models import Framework
from .serializers import FrameworkSerializer, FrameworkLikesSerializer



class FrameworkList(ListAPIView):
    queryset = Framework.objects.all()
    serializer_class = FrameworkSerializer
    #def get_queryset(self):


class FrameworkLikesCreateView(APIView):
    '''
    API to post like if is there is no likes from user for this particular asset(201) and to delete it
    if there was any(204).
    '''

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        id = self.kwargs.get('id')
        return Framework.objects.filter(id=id)


    def get(self, request, format=None, *args, **kwargs):
        """
        Returns list of users liked asset
        :param request:
        :param format:
        :return:
        """
        id = self.kwargs.get('id')
        framework = Framework.objects.get(id=id)
        serializer = FrameworkLikesSerializer(framework)
        return Response(data=serializer.data)


    def post(self, request, format=None, *args, **kwargs):
        #TODO: Protect from liking by owner
        serializer = FrameworkLikesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # entry = Entry.objects.get(id = kwargs['id'])
        try:
            entry = Framework.objects.get(likes=request.user, id=kwargs['id'])
        except Framework.DoesNotExist:
            print('Failed')
            entry = None
        if entry:
            entry.likes.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            entry = Framework.objects.get(id=kwargs['id'])
            entry.likes.add(request.user)
            # serializer.save(users_liked = request.user, id = kwargs['id'])
            return Response(status=status.HTTP_201_CREATED)
