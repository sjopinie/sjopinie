from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets

from .serializers import SubjectSerializer
from .models import Subject


# Create your views here.
def meme_page(request):
    return render(request, "sjopinie_app/meme.html")


def home_page(request):
    return render(request, "sjopinie_app/home.html")


def list_subj_page(request):
    return render(request, "sjopinie_app/list.html")


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer
