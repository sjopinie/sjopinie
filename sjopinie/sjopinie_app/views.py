from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.views import LoginView
from django.db.models import Q

from rest_framework import viewsets

from .serializers import LecturerSerializer, OpinionSerializer, SubjectSerializer, SubjectFullSerializer, TagSerializer
from .models import Lecturer, Opinion, Subject, Tag


# Create your views here.
def meme_page(request: HttpRequest):
    return render(request, "sjopinie_app/meme.html")


def home_page(request: HttpRequest):
    return render(request, "sjopinie_app/home.html")


def list_subj_page(request: HttpRequest):
    return render(request, "sjopinie_app/list.html")


def subject(request: HttpRequest, id):
    subject = Subject.objects.get(id=3)
    serializer = SubjectFullSerializer(subject)
    return JsonResponse(serializer.data)


def opinion_of_subject(request: HttpRequest, subject_id):
    opinions = Opinion.objects.filter(subject_of_opinion=subject_id)
    serializer = OpinionSerializer(opinions, many=True)
    return JsonResponse(serializer.data, safe=False)


class LecturerViewSet(viewsets.ModelViewSet):
    serializer_class = LecturerSerializer

    def get_queryset(self):
        lecturer_id = self.request.query_params.get('id')
        if lecturer_id is not None:
            return Lecturer.objects.filter(id=lecturer_id)

        q = Q()
        subject_id = self.request.query_params.get('subject_id')
        if subject_id is not None:
            q &= Q(lecturer_of_opinion__subject_of_opinion_id=subject_id)
        queryset = Lecturer.objects.filter(q)
        return queryset


class UserLogin(LoginView):
    template_name = 'sjopinie_app/login.html'


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
