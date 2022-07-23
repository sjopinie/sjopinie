from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count, IntegerField, Q
from django.utils import timezone

from rest_framework import serializers

from .models import Lecturer, Opinion, Vote, Subject, Tag


class LecturerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Lecturer
        fields = ('id', 'full_name')


class LecturerSummarizedSerializer(serializers.HyperlinkedModelSerializer):

    notes = serializers.SerializerMethodField()

    class Meta:
        model = Lecturer
        fields = ('id', 'full_name', 'notes')
        read_only_fields = ['notes']

    def get_notes(self, obj: Lecturer):
        return Opinion.objects.filter(lecturer_of_opinion=obj.id).aggregate(
            note_interesting=Avg("note_interesting",
                                 output_field=IntegerField()),
            note_easy=Avg("note_easy", output_field=IntegerField()),
            note_useful=Avg("note_useful", output_field=IntegerField()))


class OpinionSerializer(serializers.ModelSerializer):
    votes_up = serializers.SerializerMethodField()
    votes_down = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    lecturer_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    publish_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Opinion
        fields = [
            'id', 'author_name', 'opinion_text', 'note_interesting',
            'note_easy', 'note_useful', 'votes_up', 'votes_down', 'author',
            'publish_time', 'lecturer_of_opinion', 'lecturer_name',
            'subject_of_opinion', 'subject_name'
        ]
        read_only_fields = [
            'author_name', 'votes_up', 'votes_down', 'author', 'publish_time',
            'subject_name'
        ]

    def get_votes_up(self, obj: Opinion):
        value = Vote.objects.filter(opinion=obj.id).aggregate(
            votes_up=Count("value", filter=Q(value=1)))
        return value["votes_up"]

    def get_votes_down(self, obj: Opinion):
        value = Vote.objects.filter(opinion=obj.id).aggregate(
            votes_down=Count("value", filter=Q(value=-1)))
        return value["votes_down"]

    def get_author_name(self, obj: Opinion):
        return obj.author.username

    def get_subject_name(self, obj: Opinion):
        return obj.subject_of_opinion.name

    def get_lecturer_name(self, obj: Opinion):
        return obj.lecturer_of_opinion.full_name

    def create(self, validated_data: dict):
        author_model = self.context['request'].user
        if author_model.id is None:
            raise PermissionDenied
        result = Opinion.objects.create(author=author_model, **validated_data)
        return result


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class SubjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'tags')


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('value', 'author', 'opinion')


class SubjectFullSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    tag_list = serializers.CharField(max_length=200, required=False)
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ('id', 'name', 'tags', 'tag_list', 'notes', 'description',
                  'url')
        extra_kwargs = {'tag_list': {'write_only': True}}
        read_only_fields = ['notes']

    def create(self, validated_data: dict):
        tags = validated_data.get('tag_list')
        tag_models = []
        if tags:
            tag_models = self.find_tags_and_create_missing(tags)

        result = Subject.objects.create(name=validated_data['name'])
        for tag_model in tag_models:
            result.tags.add(tag_model)
        return result

    def find_tags_and_create_missing(self, tags_string: str):
        tags = tags_string.split(',')
        result = []
        for tag_name in tags:
            tag_model = None
            try:
                tag_model = Tag.objects.get(name__iexact=tag_name)
            except Tag.DoesNotExist as e:
                tag_model = Tag.objects.create(name=tag_name)
            result.append(tag_model)
        return result

    def get_notes(self, obj: Subject):
        return Opinion.objects.filter(subject_of_opinion=obj.id).aggregate(
            note_interesting=Avg("note_interesting",
                                 output_field=IntegerField()),
            note_easy=Avg("note_easy", output_field=IntegerField()),
            note_useful=Avg("note_useful", output_field=IntegerField()))
