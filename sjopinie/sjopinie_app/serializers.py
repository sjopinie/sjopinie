from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Lecturer, Opinion, Vote, Subject, Tag


class LecturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lecturer
        fields = ('id', 'full_name')


class OpinionSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Opinion
        fields = [
            'id', 'author_name', 'opinion_text', 'note_interesting',
            'note_easy', 'note_useful', 'votes_count', 'author',
            'publish_time', 'lecturer_of_opinion', 'subject_of_opinion'
        ]

    def get_votes_count(self, obj: Opinion):
        up = Vote.objects.filter(opinion=obj.id, value=1).count()
        down = Vote.objects.filter(opinion=obj.id, value=-1).count()
        return up - down

    def get_author_name(self, obj: Opinion):
        return obj.author.username


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class SubjectFullSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    tag_list = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'tags', 'tag_list')
        extra_kwargs = {'tag_list': {'write_only': True}}

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
