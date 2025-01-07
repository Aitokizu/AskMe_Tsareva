import copy

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

QUESTIONS = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'This is text for question {i}'
    } for i in range(1,30)
]


def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(
        request,
        template_name='hot_questions.html',
        context={'questions': page.object_list, 'page_obj': page }
    )

def new(request):
    new_questions = copy.deepcopy(QUESTIONS)
    new_questions.reverse()
    return render(
        request,
        template_name='new_questions.html',
        context={'questions': new_questions}
    )

def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(
        request, 'post.html',
        {'item': one_question}
    )