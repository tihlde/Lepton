from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.response import Response

from ..models import Event
from ..permissions import IsNoKorPromo
from ..serializers import EventListSerializer, EventCreateSerializer
from ..filters import EventFilter
from ..pagination import BasePagination
from app.util import yesterday


class EventViewSet(viewsets.ModelViewSet):
    """
        Display all upcoming events and filter them by title, category and expired
        Excludes expired events by default: to include expired in results, add '&expired=true'
    """
    serializer_class = EventListSerializer
    permission_classes = [IsNoKorPromo]
    queryset = Event.objects.filter(start_date__gte=yesterday()).order_by('start_date')
    pagination_class = BasePagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ['title']

    def get_queryset(self):
        if self.kwargs or 'expired' in self.request.query_params:
            return Event.objects.all().order_by('start_date')
        return Event.objects.filter(start_date__gte=yesterday()).order_by('start_date')

    def update(self, request, pk, *args, **kwargs):
        """ Updates fields passed in request """
        try:
            event = Event.objects.get(pk=pk)
            self.check_object_permissions(self.request, event)
            serializer = EventListSerializer(event, data=request.data, partial=True, many=False)

            if serializer.is_valid():
                serializer.save()
                return Response({'detail': _('Event successfully updated.')}, status=204)
            else:
                return Response({'detail': _('Could not perform update')}, status=400)

        except Event.DoesNotExist:
            return Response({'detail': 'Could not find event'}, status=400)

    def create(self, request, *args, **kwargs):
        try:
            serializer = EventCreateSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'Event created'}, status=201)
            else:
                return Response({'detail': serializer.errors}, status=400)
        except ValidationError as e:
            return Response({'detail': _(e)}, status=400)
