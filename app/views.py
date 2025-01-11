from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Tag, Question


QUESTIONS = [
    {'title': f'title {i}', 'id': i, 'text': f'This is text for question {i}'}
    for i in range(1, 30)
]


def index(request):
    page = paginate(QUESTIONS, request, per_page=5)
    return render(request, 'hot_questions.html', {'questions': page.object_list, 'page_obj': page})


def new(request):
    new_questions = QUESTIONS[::-1]
    page = paginate(new_questions, request, per_page=5)
    return render(request, 'new_questions.html', {'questions': page.object_list, 'page_obj': page})


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


def profile_settings(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')


        user = request.user
        user.username = username
        user.email = email
        user.profile.bio = bio
        user.save()
        user.profile.save()

        return redirect('profile_settings')


    user = request.user
    return render(request, 'profile_settings.html', {'user': user})


def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def tag_questions(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.filter(tags=tag)
    return render(
        request,
        'questions_by_tag.html',
        {'tag': tag, 'questions': questions}
    )