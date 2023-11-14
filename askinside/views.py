from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from templates import layouts


# Create your views here.
def index(request):

    return render(request, 'question_page.html')


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page', 1)

    return paginator.get_page(page_number)
