from re import template
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.db.models import Q
from django.views.generic.edit import CreateView

from rest_framework import viewsets

from .forms import SignUpForm
from .serializers import LecturerSerializer, OpinionSerializer, SubjectSerializer, SubjectFullSerializer, TagSerializer
from .models import Lecturer, Opinion, Subject, Tag


@login_required(login_url="/login")
def home_page(request: HttpRequest):
    return render(request, "sjopinie_app/home.html")


@login_required(login_url="/login")
def list_subj_page(request: HttpRequest):
    return render(request, "sjopinie_app/list.html")


@login_required(login_url="/login")
def subject(request: HttpRequest, id):
    subject = Subject.objects.get(id=id)
    serializer = SubjectFullSerializer(subject)

    opinions = Opinion.objects.filter(subject_of_opinion=id)
    opinion_serializer = OpinionSerializer(opinions, many=True)
    context_data = serializer.data
    opinions = opinion_serializer.data
    for opinion in opinions:
        opinion["lecturer_name"] = Lecturer.objects.get(
            id=opinion["lecturer_of_opinion"]).full_name
    context_data["opinions"] = opinions
    return render(request, "sjopinie_app/subject.html", context=context_data)


@login_required(login_url="/login")
def lecturer(request: HttpRequest, id):
    lecturer = Lecturer.objects.get(id=id)
    serializer = LecturerSerializer(lecturer)

    opinions = Opinion.objects.filter(lecturer_of_opinion=id)
    opinion_serializer = OpinionSerializer(opinions, many=True)
    context_data = serializer.data
    opinions = opinion_serializer.data
    for opinion in opinions:
        opinion["subject_name"] = Subject.objects.get(
            id=opinion["subject_of_opinion"]).name
    context_data["opinions"] = opinions
    return render(request, "sjopinie_app/lecturer.html", context=context_data)


@login_required(login_url="/login")
def search(request: HttpRequest, query: str):
    lecturers = Lecturer.objects.filter(full_name__contains=query)
    subjects = Subject.objects.filter(name__contains=query)
    lecturers_data = LecturerSerializer(lecturers, many=True).data
    for lect in lecturers_data:
        lect["opinion_count"] = Opinion.objects.filter(
            lecturer_of_opinion=lect["id"]).count()
    subjects_data = SubjectSerializer(subjects, many=True).data
    for sub in subjects_data:
        sub["opinion_count"] = Opinion.objects.filter(
            subject_of_opinion=sub["id"]).count()
    context_data = {
        "lecturers": lecturers_data,
        "subjects": subjects_data,
        "query": query
    }
    return render(request,
                  "sjopinie_app/search_results.html",
                  context=context_data)


class LecturerViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
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


class OpinionViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = OpinionSerializer

    def get_queryset(self):
        opinion_id = self.request.query_params.get('id')
        if opinion_id is not None:
            return Opinion.objects.filter(id=opinion_id)

        query = Q()
        subject_id = self.request.query_params.get('subject_id')
        if subject_id is not None:
            query &= Q(subject_of_opinion=subject_id)

        lecturer_id = self.request.query_params.get('lecturer_id')
        if lecturer_id is not None:
            query &= Q(lecturer_of_opinion=lecturer_id)

        return Opinion.objects.filter(query)


class UserLoginView(LoginView):
    template_name = 'sjopinie_app/login.html'


class UserSignUpView(CreateView):
    form_class = SignUpForm
    success_url = "/login"
    template_name = 'sjopinie_app/signup.html'


class SubjectViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')

    def get_serializer_class(self):
        if self.action == 'create':
            return SubjectFullSerializer
        return SubjectSerializer


class TagViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer


class LecturerCreateView(LoginRequiredMixin, CreateView):
    model = Lecturer
    fields = "__all__"
    success_url = "/new/opinion"
    template_name = 'sjopinie_app/base_create_form.html'


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    fields = "__all__"
    success_url = "/"
    template_name = 'sjopinie_app/base_create_form.html'


class OpinionCreateView(LoginRequiredMixin, CreateView):
    model = Opinion
    success_url = "/"
    template_name = 'sjopinie_app/opinion_create_form.html'
    fields = [
        'subject_of_opinion', 'lecturer_of_opinion', 'opinion_text',
        'note_interesting', 'note_easy', 'note_useful'
    ]
