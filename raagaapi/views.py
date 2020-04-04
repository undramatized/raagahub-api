from django.shortcuts import render

from rest_framework import viewsets, generics, filters

from .serializers import RagaSerializer
from .models import Raga


class SwaraFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        swaras = request.query_params.get('swaras', None)
        if swaras:
            return Raga.objects.filter_swaras_queryset(swaras, queryset)
        else:
            return queryset

    def to_html(self, request, queryset, view):
        pass

# ragas/ => Returns all ragas
# ragas/?search=char => Returns ragas starting with search string
# ragas/?swaras=S%20R2%20G2 => Returns ragas containing those swaras
class RagaViewSet(viewsets.ModelViewSet):
    """
    Return a list of all the existing ragas.
    """
    queryset = Raga.objects.all().order_by('format_name')
    serializer_class = RagaSerializer
    filter_backends = (filters.SearchFilter, SwaraFilterBackend, )
    search_fields = ['^format_name', '^name']
    filter_fields = ['swaras']