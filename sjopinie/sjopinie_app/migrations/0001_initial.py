# Generated by Django 4.0.4 on 2022-07-23 13:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=80, unique=True, verbose_name='Imię i nazwisko')),
            ],
            options={
                'verbose_name': 'Prowadzący',
                'verbose_name_plural': 'Prowadzący',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Tagi',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nazwa')),
                ('tags', models.ManyToManyField(related_name='tags', to='sjopinie_app.tag', verbose_name='Tagi')),
            ],
            options={
                'verbose_name': 'Lektorat',
                'verbose_name_plural': 'Lektoraty',
            },
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opinion_text', models.CharField(max_length=5000, verbose_name='Tekst')),
                ('semester', models.CharField(blank=True, choices=[(1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V'), (6, 'VI'), (7, 'VII'), (8, 'VIII'), (9, 'IX')], max_length=5, null=True, verbose_name='Semestr')),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('note_interesting', models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Jak interesujący')),
                ('note_easy', models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Jak łatwy')),
                ('note_useful', models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Jak użyteczny')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='autor')),
                ('lecturer_of_opinion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecturer_of_opinion', to='sjopinie_app.lecturer', verbose_name='Prowadzący')),
                ('subject_of_opinion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_of_opinion', to='sjopinie_app.subject', verbose_name='Lektorat')),
            ],
            options={
                'verbose_name': 'Opinia',
                'verbose_name_plural': 'Opinie',
                'unique_together': {('author', 'subject_of_opinion', 'lecturer_of_opinion')},
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, '+1'), (-1, '-1')])),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('opinion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sjopinie_app.opinion')),
            ],
            options={
                'unique_together': {('author', 'opinion')},
            },
        ),
    ]
