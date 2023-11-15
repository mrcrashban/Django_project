from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse

from askinside.models import Tag, Question, Answer
from templates import layouts


# Create your views here.
def main_page(request):
    page_obj = paginate(Question.objects.sorted_by_created_at(), request)

    context = {'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               }

    return render(request, 'main_page.html', context)


def hot(request):
    page_obj = paginate(Question.objects.sorted_by_rating(), request)
    context = {'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               }

    return render(request, 'hot.html', context)


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def new_question(request):
    context = {'global_tags': Tag.objects.sort_by_related_question_quantity()[:10]}

    return render(request, 'ask.html', context)


def settings(request):
    return render(request, 'settings.html')


def question_page(request, question_id):
    page_obj = paginate(Answer.objects.filter(question_id=question_id), request, 3)

    context = {'question': Question.objects.get(pk=question_id),
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               'page_obj': page_obj,
               }
    return render(request, 'question_page.html', context)


def tag(request, title):
    page_obj = paginate(Question.objects.filter_by_tag(title), request)

    context = {'tag': Tag.objects.get(title=title),
               'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10]
               }
    return render(request, 'show_tag.html', context)


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page', 1)

    return paginator.get_page(page_number)
