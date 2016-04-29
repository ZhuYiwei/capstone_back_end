from datetime import date
from django import forms
from django.contrib.auth import authenticate
from django.forms.extras import SelectDateWidget
from ipm.models import *

__author__ = 'Yiwei'


class PatentForm(forms.ModelForm):
    class Meta:
        model = Patent
        exclude = ('created_date', 'latest_date')

        year_now = date.today().year + 1
        year_begin = year_now - 20
        widgets = {
            'filing_date': SelectDateWidget(years=range(year_begin, year_now)),
            'priority_date': SelectDateWidget(years=range(year_begin, year_now)),
            'hearing_date': SelectDateWidget(years=range(year_begin, year_now)),
            'publication_date': SelectDateWidget(years=range(year_begin, year_now)),
            'abstract': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super(PatentForm, self).__init__(*args, **kwargs)
        date_list = ['filing_date', 'priority_date', 'hearing_date', 'publication_date']
        for field in self.fields:
            if field not in date_list:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super(PatentForm, self).clean()
        application_number = str(cleaned_data.get('application_number')).strip()
        if Patent.objects.filter(application_number__exact=application_number):
            raise forms.ValidationError("This Application Number is already existed")

        cleaned_data['application_number'] = application_number
        return cleaned_data


class PatentEditForm(PatentForm):
    class Meta(PatentForm.Meta):
        exclude = ('application_number', 'created_date', 'latest_date')

    def clean(self):
        cleaned_data = super(PatentForm, self).clean()
        return cleaned_data


class InsightForm(forms.ModelForm):
    class Meta:
        model = Insight
        exclude = ('create_date', 'modified_date')

    def __init__(self, *args, **kwargs):
        super(InsightForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
