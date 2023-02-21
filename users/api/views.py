from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes


@api_view(('GET',))
def index(request):
    return Response({})
