from re import template
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.db.models import Q
from django.views.generic.edit import CreateView

from rest_framework import mixins, viewsets

from sjopinie_account.utils import log_action, ADDITION

from .forms import SignUpForm
from .serializers import LecturerSerializer, LecturerSummarizedSerializer, OpinionSerializer, SubjectSerializer, SubjectFullSerializer, TagSerializer, VoteSerializer
from .models import Lecturer, Opinion, Subject, Tag, Vote

from allauth.account.decorators import login_required


@login_required(login_url="/login")
def home_page(request: HttpRequest):
    return render(request, "sjopinie_app/home.html")


@login_required(login_url="/login")
def subject(request: HttpRequest, id):
    subject = Subject.objects.get(id=id)
    serializer = SubjectFullSerializer(subject)

    opinions = Opinion.objects.filter(subject_of_opinion=id)[0:10]
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
    serializer = LecturerSummarizedSerializer(lecturer)

    loaded_opinions_count = 10
    opinions = Opinion.objects.filter(
        lecturer_of_opinion=id)[0:loaded_opinions_count]
    opinion_serializer = OpinionSerializer(opinions, many=True)
    context_data = serializer.data
    opinions = opinion_serializer.data
    context_data["opinions"] = opinions
    return render(request, "sjopinie_app/lecturer.html", context=context_data)


@login_required(login_url="/login")
def search(request: HttpRequest, query: str):
    lecturers = Lecturer.objects.filter(full_name__contains=query)
    q = Q(tags__name__contains=query)
    q |= Q(name__contains=query)
    subjects = Subject.objects.filter(q)
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


class VoteViewSet(LoginRequiredMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def create(self, request, *args, **kwargs):
        votes = Vote.objects.filter(author=request.user,
                                    opinion=request.data['opinion'])
        if votes.count():
            vote = votes[0]
            if int(request.data['value']) != vote.value:
                vote.value = request.data['value']
                vote.save()
                return HttpResponse("Vote updated successfully")
            return HttpResponse()
        request.data["author"] = request.user.id
        return super().create(request, *args, **kwargs)


class LogCreateView(CreateView):

    def form_valid(self, form) -> HttpResponse:
        result = super().form_valid(form)  #it creates resulting self.object
        o = self.object
        u = self.request.user
        log_action(u, o, action_flag=ADDITION)
        return result


class LecturerCreateView(LoginRequiredMixin, LogCreateView):
    model = Lecturer
    fields = "__all__"
    success_url = "/new/opinion"
    template_name = 'sjopinie_app/base_create_form.html'


class SubjectCreateView(LoginRequiredMixin, LogCreateView):
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

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        log_action(
            obj.author,
            obj,
            repr(obj),
            ADDITION,
        )
        return HttpResponseRedirect(self.success_url)
