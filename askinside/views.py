from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from templates import layouts

questions = [
    {
        'title': f'Question {i}',
        'body': f'Long lorem ipsum {i}',
        'votes': i,
        'created_at': i,
        'tags': f'Python',
        'author': f'Anton {i}'
    } for i in range(30)
]

tags = [
    {
        'title': f'Python',
        'created_at': j
    } for j in range(3)
]


# Create your views here.
def main_page(request):
    page_obj = paginate(questions, request)
    context = {'page_obj': page_obj,
               'global_tags': tags,
               }
    return render(request, 'main_page.html', context)


def hot(request):
    page_obj = paginate(questions, request)
    context = {'page_obj': page_obj,
               'global_tags': tags,
               }
    return render(request, 'hot.html', context)


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def new_question(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')


def question_page(request):
    return render(request, 'question_page.html')

def tag(request):
    return render(request, 'show_tag.html')

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page', 1)

    return paginator.get_page(page_number)
