from rest_framework import serializers

from .models import Lecturer, Opinion, Vote, Subject, Tag


class LecturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lecturer
        fields = ('id', 'name', 'surname')


class OpinionSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Opinion
        fields = ('id', 'opinion_text', 'note_interesting', 'note_easy',
                  'note_useful', 'votes_count')

    def get_votes_count(self, obj: Opinion):
        up = Vote.objects.filter(opinion=obj.id, value=1).count()
        down = Vote.objects.filter(opinion=obj.id, value=-1).count()
        return up - down


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
