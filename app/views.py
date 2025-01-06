import copy

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
    return render(
        request,
        template_name='hot_questions.html',
        context={'questions': QUESTIONS }
    )

def new(request):
    new_questions = copy.deepcopy(QUESTIONS)
    new_questions.reverse()
    return render(
        request,
        template_name='new_questions.html',
        context={'questions': new_questions}
    )
