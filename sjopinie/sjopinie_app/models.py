from django.db import models


class User(models.Model):
    login = models.CharField(max_length=200, primary_key=True)
    hash_of_password = models.CharField(max_length=255, blank=True)
    date_of_registration = models.DateTimeField()


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Lecturer(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    academic_title = models.CharField(max_length=20)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name="tags")

    def __str__(self):
        return self.name


class Opinion(models.Model):
    SEMESTER_VALUES = ((1, "I"), (2, "II"), (3, "III"), (4, "IV"), (5, "V"),
                       (6, "VI"), (7, "VII"), (8, "VIII"), (9, "IX"))
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    opinion_text = models.CharField(max_length=5000)
    semester = models.CharField(max_length=5,
                                null=True,
                                choices=SEMESTER_VALUES)
    publish_time = models.DateTimeField(default="2021-01-01 00:00:00")
    subject_of_opinion = models.ForeignKey(Subject,
                                           null=True,
                                           on_delete=models.SET_NULL)
    lecturer_of_opinion = models.ForeignKey(Lecturer,
                                            null=True,
                                            on_delete=models.SET_NULL)


class Vote(models.Model):
    VOTE_VALUES = (
        (1, '+1'),
        (-1, '-1'),
    )
    value = models.IntegerField(choices=VOTE_VALUES)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    opinion = models.ForeignKey(Opinion, null=True, on_delete=models.SET_NULL)
