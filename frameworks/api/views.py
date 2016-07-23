from rest_framework.generics import ListAPIView


from ..models import Framework
from .serializers import FrameworkSerializer



class FrameworkList(ListAPIView):
    queryset = Framework.objects.all()
    serializer_class = FrameworkSerializer

    #def get_queryset(self):
