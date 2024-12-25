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
        template_name='vanilla.html',
        context={'questions': QUESTIONS }
    )
