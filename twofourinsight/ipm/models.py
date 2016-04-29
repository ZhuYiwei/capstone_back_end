from datetime import date
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.template.backends import django
from django.utils import timezone
from django_countries.fields import CountryField
from django.db.models import Q
# pip install django-countries

STATUS_CHOICES = [[1, 'GRANTED'], [2, 'REFUSED'], [3, 'PENDING']]
CATEGORY_CHOICES = [[1, 'PHARMACEUTICALS'], [2, 'MEDICAL DEVICES & DIAGNOSTICS'], [3, 'BIOTECHNOLOGY & VACCINES']]
SEARCH_FIELDS = ('applicant_name', 'application_number', 'title_of_invention', 'abstract')
INSIGHT_SEARCH_FIELDS = ('content', 'title')


class Patent(models.Model):
    # required fields
    applicant_name = models.CharField(max_length=100, null=False, blank=False, default="")
    application_number = models.CharField(max_length=20, null=False, blank=False, unique=True, default="")
    title_of_invention = models.CharField(max_length=500, null=False, blank=False, default="")

    hearing_date = models.DateField(null=True, blank=True)
    priority_date = models.DateField(null=True, blank=True)
    filing_date = models.DateField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    created_date = models.DateField(auto_now=True, null=True)
    latest_date = models.DateField(null=True, blank=True)

    abstract = models.TextField(null=True, blank=True)
    PCT_number = models.CharField(max_length=20, null=True, blank=True)
    category_code = models.IntegerField(null=True, blank=True, choices=CATEGORY_CHOICES)

    status_with_US_EPO = models.CharField(null=True, blank=True, max_length=50)
    link = models.URLField(null=True, blank=True)
    priority_country = models.CharField(max_length=20, null=True, blank=True)

    decision = models.IntegerField(null=True, blank=True, choices=STATUS_CHOICES)
    decision_comments = models.TextField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.application_number + " - " + self.applicant_name

    @property
    def get_decision(self):
        if self.decision:
            return STATUS_CHOICES[self.decision - 1][1]
        return ""

    @property
    def category(self):
        if self.category_code:
            return CATEGORY_CHOICES[self.category_code - 1][1]
        return ""

    @property
    def get_latest_date(self):
        if not self.filing_date and not self.priority_date and not self.hearing_date and not self.publication_date:
            return ""

        the_date = datetime.date(year=datetime.datetime.today().year - 20, month=1, day=1)

        if self.filing_date and the_date < self.filing_date:
            the_date = self.filing_date
        if self.priority_date and the_date < self.priority_date:
            the_date = self.priority_date
        if self.hearing_date and the_date < self.hearing_date:
            the_date = self.hearing_date
        if self.publication_date and the_date < self.publication_date:
            the_date = self.publication_date

        return the_date

    @property
    def short(self):
        return {
            "id": self.id,
            "title_of_invention": self.title_of_invention,
            "applicant": self.applicant_name,
            "decision": self.get_decision,
        }

    @property
    def long(self):
        return {
            "id": self.id,
            "application_number": self.application_number,
            "title_of_invention": self.title_of_invention,
            "decision": self.get_decision,
            "filing_date": self.filing_date,
            "abstract": self.abstract,
            "applicant_name": self.applicant_name,
            "category": self.category,
            "PCT_number": self.PCT_number
        }

    @staticmethod
    def get_recent_list():
        return Patent.objects.order_by('-latest_date')

    @staticmethod
    def search(keyword):
        q_objs = [Q(**{'%s__icontains' % i: keyword}) for i in SEARCH_FIELDS]
        queries = reduce(lambda x, y: x | y, q_objs)
        results = Patent.objects.filter(queries)
        return results


class Insight(models.Model):
    # required fields
    patent = models.ForeignKey(Patent, default="")
    title = models.CharField(max_length=500, null=False, blank=False, default="")
    content = models.TextField(null=False, blank=False, default="")
    link = models.URLField(default="http://twofourinsight.com/", blank=True)
    # priority_country = CountryField()

    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title + " - " + self.create_date.__str__()

    @property
    def short(self):
        return {
            "id": self.id,
            "title": self.title,
            "create_date": self.create_date.date(),
            "url": self.link,
        }

    @property
    def long(self):
        return {
            "id": self.id,
            "title": self.title,
            "create_date": self.create_date.date(),
            "content": self.content,
            "patent": self.patent.title_of_invention
        }

    @staticmethod
    def search(keyword):
        q_objs = [Q(**{'%s__icontains' % i: keyword}) for i in INSIGHT_SEARCH_FIELDS]
        queries = reduce(lambda x, y: x | y, q_objs)
        results = Insight.objects.filter(queries)
        return results
