from rest_framework import viewsets
from rest_framework import renderers
from rest_framework_extensions.mixins import DetailSerializerMixin
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.settings import api_settings

from rest_framework_xml.renderers import XMLRenderer

from .renderers import PaginatedCSVRenderer
from .pagination import HALPagination
from .serializers import (  # noqa: F401
    DisplayField, DataSetSerializerMixin, get_links,
    HALSerializer, LinksField, RelatedSummaryField,
    SelfLinkSerializerMixin
)

DEFAULT_RENDERERS = [
    renderers.JSONRenderer,
    PaginatedCSVRenderer,
    renderers.BrowsableAPIRenderer,
    XMLRenderer,
]


if api_settings.DEFAULT_RENDERER_CLASSES:
    DEFAULT_RENDERERS = api_settings.DEFAULT_RENDERER_CLASSES


class _DisabledHTMLFilterBackend(DjangoFilterBackend):
    """
    See https://github.com/tomchristie/django-rest-framework/issues/3766
    This prevents DRF from generating the filter dropdowns (which can be HUGE
    in our case)
    """

    def to_html(self, request, queryset, view):
        return ""


class DatapuntViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet subclass for use in Datapunt APIs.

    Note:
    - this uses HAL JSON style pagination.
    """
    renderer_classes = DEFAULT_RENDERERS
    pagination_class = HALPagination
    filter_backends = (_DisabledHTMLFilterBackend,)
    # TO restore filter box in your view!
    # filter_backends = (DjangoFilterBackend,)

    detailed_keyword = 'detailed'

    def list(self, request, *args, **kwargs):
        # Checking if a detailed response is required
        if request.GET.get(self.detailed_keyword, False):
            self.serializer_class = self.serializer_detail_class
        return super().list(self, request, *args, **kwargs)


class DatapuntViewSetWritable(DetailSerializerMixin, viewsets.ModelViewSet):
    """
    ViewSet subclass for use in Datapunt APIs.

    Note:
    - this uses HAL JSON style pagination.
    """
    renderer_classes = DEFAULT_RENDERERS
    pagination_class = HALPagination

    filter_backends = (_DisabledHTMLFilterBackend,)
