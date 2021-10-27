from rest_framework import serializers

from .models import Lecturer, Subject, Tag


class LecturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lecturer
        fields = ('id', 'name', 'surname')


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class SubjectFullSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'tags')
