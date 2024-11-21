import copy
from http.client import HTTPResponse

from django.shortcuts import render

QUESTIONS = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'question number {i}'
    } for i in range(1,30)
]
def index(request):
    return render(
        request, 'index.html',
        context={'questions': QUESTIONS}
    )

