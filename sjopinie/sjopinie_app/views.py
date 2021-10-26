from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets

from .serializers import SubjectSerializer, SubjectFullSerializer, TagSerializer
from .models import Subject, Tag

import logging

logger = logging.getLogger(__name__)


# Create your views here.
def meme_page(request):
    return render(request, "sjopinie_app/meme.html")


def home_page(request):
    return render(request, "sjopinie_app/home.html")


def list_subj_page(request):
    return render(request, "sjopinie_app/list.html")


def subject(request, id):
    logger.error('Something went wrong!')
    subject = Subject.objects.get(id=3)
    serializer = SubjectFullSerializer(subject)
    return JsonResponse(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
