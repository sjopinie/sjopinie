from rest_framework import serializers

from .models import Subject


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')


class SubjectFullSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')
