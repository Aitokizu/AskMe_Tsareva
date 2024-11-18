import copy
from http.client import HTTPResponse

from django.shortcuts import render

QUESTIONS = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'question number {i}'
    } for i in range(30)
]
def index(request):
    return render(
        request, 'index.html',
        context={'questions': QUESTIONS}
    )
def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(
        request, 'one_question.html',
        context={'item': one_question}
    )

def new(request):
    new_questions= copy.deepcopy(QUESTIONS)
    new_questions.reverse()
    return render(
        request, 'new.html',
        context={'questions': new_questions}
    )

