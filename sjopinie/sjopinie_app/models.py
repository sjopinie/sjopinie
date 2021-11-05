from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Lecturer(models.Model):
    full_name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.full_name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name="tags")

    def __str__(self):
        return self.name


class Opinion(models.Model):
    SEMESTER_VALUES = ((1, "I"), (2, "II"), (3, "III"), (4, "IV"), (5, "V"),
                       (6, "VI"), (7, "VII"), (8, "VIII"), (9, "IX"))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    opinion_text = models.CharField(max_length=5000)
    semester = models.CharField(max_length=5,
                                blank=True,
                                null=True,
                                choices=SEMESTER_VALUES)
    publish_time = models.DateTimeField(auto_now_add=True)
    subject_of_opinion = models.ForeignKey(Subject,
                                           on_delete=models.CASCADE,
                                           related_name="subject_of_opinion")
    lecturer_of_opinion = models.ForeignKey(Lecturer,
                                            on_delete=models.CASCADE,
                                            related_name="lecturer_of_opinion")
    note_interesting = models.SmallIntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(100),
                    MinValueValidator(1)])
    note_easy = models.SmallIntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(100),
                    MinValueValidator(1)])
    note_useful = models.SmallIntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(100),
                    MinValueValidator(1)])

    def __str__(self):
        return f"{self.author} Subject: {self.subject_of_opinion} {self.publish_time}"


class Vote(models.Model):
    VOTE_VALUES = (
        (1, '+1'),
        (-1, '-1'),
    )
    value = models.IntegerField(choices=VOTE_VALUES)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    opinion = models.ForeignKey(Opinion, null=True, on_delete=models.CASCADE)
