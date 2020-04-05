from django.shortcuts import render

from rest_framework import viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import RagaSerializer, ChordSerializer
from .models import Raga, Chord


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

    @action(detail=True, url_path='chords', url_name='chords')
    def get_chords(self, request, pk=None):
        """
        Return a list of all the defined chords, for a particular raga and root note (default C)
        """
        raga = Raga.objects.get(pk=pk)
        root = request.query_params.get('root', 'C')

        chord_list = raga.get_chords(root)
        return Response(chord_list)

# chords/ => Returns all chords
class ChordViewSet(viewsets.ModelViewSet):
    """
    Return a list of all the defined chords.
    """
    queryset = Chord.objects.all()
    serializer_class = ChordSerializer