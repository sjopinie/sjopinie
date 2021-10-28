from rest_framework import serializers

from .models import Lecturer, Opinion, Subject, Tag


class LecturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lecturer
        fields = ('id', 'name', 'surname')


class OpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = ('id', 'opinion_text', 'note_interesting', 'note_easy',
                  'note_useful')


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
