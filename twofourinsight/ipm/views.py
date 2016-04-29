from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction
from ipm.forms import *
from ipm.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse, StreamingHttpResponse, HttpResponseNotAllowed, \
    JsonResponse, HttpResponseBadRequest
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.staticfiles.templatetags.staticfiles import static


def home(request):
    patents = Patent.get_recent_list()
    insights = Insight.objects.order_by('-id')
    context = {'patents': patents, 'insights': insights}
    return render(request, "home.html", context)


def get_patents(request):
    patents = Patent.get_recent_list()
    context = {'patents': patents}
    return render(request, "patents.html", context)


def get_insights(request):

    insights = Insight.objects.order_by('-id')
    context = {'insights': insights}
    return render(request, "insights.html", context)


def add(request):
    context = {'patent_form': PatentForm(prefix='patent'), 'insight_form': InsightForm(prefix='insight')}
    return render(request, "add.html", context)


@transaction.atomic
def add_patent(request):
    if request.method == 'GET':
        return redirect(reverse(add))

    patent_form = PatentForm(request.POST, prefix='patent')
    if patent_form.is_valid():
        print 'patent form is valid'
        new_patent = patent_form.save()
        new_patent.save()
        new_patent.latest_date = new_patent.get_latest_date
        new_patent.save()

        return redirect(reverse(add))

    # not valid, return the error form
    print 'patent form is NOT valid'
    context = {'patent_form': patent_form, 'insight_form': InsightForm(prefix='insight')}
    return render(request, "add.html", context)


def delete_patent(request, patent_id):
    to_delete = get_object_or_404(Patent, id=patent_id)
    to_delete.delete()
    return redirect(reverse('get_patents'))


def delete_insight(request, insight_id):
    to_delete = get_object_or_404(Insight, id=insight_id)
    to_delete.delete()
    return redirect(reverse('get_insights'))


@transaction.atomic
def edit_patent(request, patent_id):
    try:
        if request.method == 'GET':
            patent = Patent.objects.get(id=patent_id)
            context = {'form': PatentEditForm(instance=patent, prefix='patent'), 'action_url': 'edit_patent',
                       'param': patent_id}
            return render(request, 'edit.html', context)

        patent = Patent.objects.select_for_update().get(id=patent_id)
        patent_form = PatentEditForm(request.POST, instance=patent, prefix='patent')

        if patent_form.is_valid():
            print 'patent form is valid'
            patent_form.save()
            # patent.latest_date = patent.get_latest_date()
            patent.save()
            if patent.get_latest_date:
                patent.latest_date = patent.get_latest_date
                patent.save()
            return redirect(reverse('get_patents'))

        print 'edit patent form not valid'
        context = {'form': patent_form, 'action_url': 'edit_patent', 'param': patent_id}
        return render(request, 'edit.html', context)

    except ObjectDoesNotExist:
        print 'No such Profile'
        return redirect(reverse(home))


@transaction.atomic
def add_insight(request):
    if request.method == 'GET':
        return redirect(reverse(add))

    insight_form = InsightForm(request.POST, prefix='insight')
    if insight_form.is_valid:
        print 'insight form is valid'
        new_insight = insight_form.save()
        new_insight.save()
        return redirect(reverse(add))

    # not valid, return the error form
    context = {'patent_form': PatentForm(prefix='patent'), 'insight_form': insight_form}
    return render(request, "add.html", context)


@transaction.atomic
def edit_insight(request, insight_id):
    try:
        if request.method == 'GET':
            insight = Insight.objects.get(id=insight_id)
            context = {'form': InsightForm(instance=insight, prefix='insight'), 'action_url': 'edit_insight',
                       'param': insight_id}
            return render(request, 'edit.html', context)

        insight = Insight.objects.select_for_update().get(id=insight_id)
        insight_form = InsightForm(request.POST, instance=insight, prefix='insight')

        if insight_form.is_valid():
            print 'insight edit form is valid'
            insight_form.save()
            return redirect(reverse('get_insights'))

        print 'edit patent form not valid'
        context = {'form': insight_form, 'action_url': 'edit_patent', 'param': insight_id}
        return render(request, 'edit.html', context)

    except ObjectDoesNotExist:
        print 'No such Profile'
        return redirect(reverse(home))


def get_patent_list(request):
    if request.method != 'GET':
        response = HttpResponseNotAllowed(['GET'])
        response.write("Error: only GET method is allowed")
        return response

    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    decision = request.GET.get('status')

    patents = Patent.get_recent_list()

    if category:
        if category.isdigit():
            category = int(category)
            patents = patents.filter(category_code=category)

    if decision:
        if decision.isdigit():
            decision = int(decision)
            patents = patents.filter(decision=decision)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            patents = patents.filter(latest_date__gte=start_date)
        except ValueError:
            return HttpResponseBadRequest

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            patents = patents.filter(latest_date__lte=end_date)
        except ValueError:
            return HttpResponseBadRequest

    data = {
        "patents": [p.short for p in patents]
    }
    return JsonResponse(data)


def get_patent(request, patent_id):
    if request.method != 'GET':
        response = HttpResponseNotAllowed(['GET'])
        response.write("Error: only GET method is allowed")
        return response

    patent = get_object_or_404(Patent, id=patent_id)

    data = {
        "patent": patent.long
    }

    return JsonResponse(data)


def get_patent_model(request, patent_id):
    if request.method != 'GET':
        response = HttpResponseNotAllowed(['GET'])
        response.write("Error: only GET method is allowed")
        return response
    try:
        patent = Patent.objects.filter(id=patent_id)
        response_text = serializers.serialize('json', patent)
        return HttpResponse(response_text, content_type='application/json')
    except:
        raise Http404


def get_patent_json(request):
    if request.method != 'GET':
        response = HttpResponseNotAllowed(['GET'])
        response.write("Error: only GET method is allowed")
        return response

    patent = Patent.objects.all()
    response_text = serializers.serialize('json', patent)
    return HttpResponse(response_text, content_type='application/json')


def get_insight_list(request):
    if request.method != 'GET':
        response = HttpResponseNotAllowed(['GET'])
        response.write("Error: only GET method is allowed")
        return response

    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('decision')

    insights = Insight.objects.order_by("-id")

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            insights = insights.filter(create_date__gte=start_date)
        except ValueError:
            return HttpResponseBadRequest

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            insights = insights.filter(create_date__lte=end_date)
        except ValueError:
            return HttpResponseBadRequest

    data = {
        "insights": [i.short for i in insights]
    }

    return JsonResponse(data)


def get_insight(request, insight_id):
    if request.method != 'GET':
        response = HttpResponseNotAllowed(['GET'])
        response.write("Error: only GET method is allowed")
        return response

    insight = get_object_or_404(Insight, id=insight_id)

    data = {
        "patent": insight.long
    }

    return JsonResponse(data)


def search_patent(request):
    if request.method != 'GET':
        response = HttpResponseNotAllowed(['GET'])
        response.write("Error: only GET method is allowed")
        return response

    keyword = request.GET.get('keyword')

    if keyword and keyword != '':
        result = Patent.search(keyword)

        data = {
            "patents": [i.short for i in result]
        }

        return JsonResponse(data)

    response = HttpResponse()
    response.write("No search_patent keyword provided")
    return response


def search_insight(request):
    if request.method != 'GET':
        response = HttpResponseNotAllowed(['GET'])
        response.write("Error: only GET method is allowed")
        return response

    keyword = request.GET.get('keyword')

    if keyword and keyword != '':
        result = Insight.search(keyword)

        data = {
            "insights": [i.short for i in result]
        }

        return JsonResponse(data)

    response = HttpResponse()
    response.write("No search_patent keyword provided")
    return response


def developer_home(request):
    return render(request, 'developer.html', {})


def send_email(request):
    if request.method != 'GET':
        response = HttpResponseNotAllowed(['GET'])
        response.write("Error: only GET method is allowed")

    email = request.GET.get("email")
    response = HttpResponse()
    if email:

        email_body = """
        The URL for the document is:
        http://%s%s""" % (request.get_host(), static('20160114-CGPDTM-DECISION-TAKEDA-833-KOLNP-2010.pdf'))

        send_mail(subject="TwoFourInsight Download",
                  message=email_body,
                  from_email="noreply@crackgmat.com",
                  recipient_list=[email])
        response.write("Send Succeed")
    else:
        response.write("Email Address is not given")

    return response


def today(request):
    patents = Patent.get_recent_list()[:1]
    insights = Insight.objects.order_by('-id')[:1]
    data = {
        "patents":  [i.short for i in patents],
        "insights": [i.short for i in insights],
    }

    return JsonResponse(data)
