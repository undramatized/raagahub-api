from rest_framework import serializers

from .models import Raga, Chord

class RagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raga
        fields = ('id',
                  'format_name',
                  'name',
                  'melakarta',
                  'arohanam',
                  'avarohanam',
                  'is_janaka',
                  'is_janya',
                  'is_vakra',
                  'is_bashanga',
                  'is_upanga'
                  )

class ChordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chord
        fields = ('id', 'name', 'description', 'formula', 'affix')