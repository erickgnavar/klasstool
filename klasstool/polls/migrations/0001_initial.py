# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 04:32
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.CharField(max_length=100, verbose_name='Value')),
            ],
            options={
                'verbose_name': 'Choice',
                'default_related_name': 'choices',
                'verbose_name_plural': 'Choices',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is active?')),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='Start')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='End')),
                ('result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Result')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='polls', to='courses.Session')),
            ],
            options={
                'verbose_name': 'Poll',
                'default_related_name': 'polls',
                'verbose_name_plural': 'Polls',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='polls.Choice')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='polls.Poll')),
            ],
            options={
                'verbose_name': 'Response',
                'default_related_name': 'responses',
                'verbose_name_plural': 'Responses',
            },
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='polls.Poll'),
        ),
    ]