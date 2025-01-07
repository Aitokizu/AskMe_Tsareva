import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render

QUESTIONS = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'This is text for question {i}'
    } for i in range(1,30)
]


def index(request):
    page = paginate(QUESTIONS, request, per_page=5)
    return render(
        request,
        template_name='hot_questions.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def new(request):
    new_questions = copy.deepcopy(QUESTIONS)
    new_questions.reverse()
    page = paginate(new_questions, request, per_page=5)
    return render(
        request,
        template_name='new_questions.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def question(request, question_id):
    one_question = next((q for q in QUESTIONS if q['id'] == question_id), None)
    if one_question is None:
        raise Http404("Question not found")
    return render(request, 'post.html', {'item': one_question})

def ask(request):
    return render(request, 'add_question.html')

def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page