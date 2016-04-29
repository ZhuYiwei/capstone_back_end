# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=500)),
                ('content', models.TextField(default=b'')),
                ('link', models.URLField(default=b'http://twofourinsight.com/', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applicant_name', models.CharField(default=b'', max_length=50)),
                ('application_number', models.CharField(default=b'', unique=True, max_length=20)),
                ('title_of_invention', models.CharField(default=b'', max_length=500)),
                ('hearing_date', models.DateField(null=True, blank=True)),
                ('priority_date', models.DateField(null=True, blank=True)),
                ('filing_date', models.DateField(null=True, blank=True)),
                ('publication_date', models.DateField(null=True, blank=True)),
                ('created_date', models.DateField(auto_now=True, null=True)),
                ('latest_date', models.DateField(null=True, blank=True)),
                ('abstract', models.TextField(null=True, blank=True)),
                ('PCT_number', models.CharField(max_length=20, null=True, blank=True)),
                ('category_code', models.IntegerField(blank=True, null=True, choices=[[1, b'PHARMACEUTICALS'], [2, b'MEDICAL DEVICES & DIAGNOSTICS'], [3, b'BIOTECHNOLOGY & VACCINES']])),
                ('status_with_US_EPO', models.CharField(max_length=50, null=True, blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('priority_country', models.CharField(max_length=20, null=True, blank=True)),
                ('decision', models.IntegerField(blank=True, null=True, choices=[[1, b'GRANTED'], [2, b'REFUSED'], [3, b'PENDING']])),
                ('decision_comments', models.TextField(max_length=500, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='insight',
            name='patent',
            field=models.ForeignKey(default=b'', to='ipm.Patent'),
        ),
    ]
