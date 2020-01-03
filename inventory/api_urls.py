from django.conf.urls import url
from django.db.models import F, Sum
from django.urls import include
from rest_framework import routers
from rest_framework.decorators import api_view, renderer_classes

from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from inventory.models import Item, Container, ItemTag
from inventory.serializers import ItemSerializer, ItemTagSerializer, ContainerSerializer


class ItemViewSet(ModelViewSet):
    def get_queryset(self):
        should_filter_restock = self.request.query_params.get('needs_restock', False)
        query = Item.objects.all()
        if should_filter_restock:
            query = query.filter(quantity__lte=F('alert_quantity'))
        return query

    serializer_class = ItemSerializer


class ContainerViewSet(ModelViewSet):
    def get_queryset(self):
        parent = self.request.query_params.get('parent', None)
        query = Container.objects.all()
        if parent:
            if parent == '-1':
                query = query.filter(parent__isnull=True)
            else:
                query = query.filter(parent__exact=parent)
        return query
    serializer_class = ContainerSerializer


class ItemTagViewSet(ModelViewSet):
    queryset = ItemTag.objects.all()
    serializer_class = ItemTagSerializer


class InfoView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            'total_item_count': Item.objects.aggregate(item_count=Sum('quantity'))['item_count'],
            'container_count': Container.objects.count()
        })


router = routers.DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'containers', ContainerViewSet, basename='container')
router.register(r'item-tags', ItemTagViewSet)


urlpatterns = [
    url(r'^info$', InfoView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]