from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, UserProfile, Tag


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаем профиль пользователя при регистрации
            UserProfile.objects.get_or_create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def index(request):
    questions = Question.objects.order_by('-likes')
    popular_tags = Tag.objects.annotate(num_questions=Count('questions')).order_by('-num_questions')[:5]
    top_mentors = UserProfile.objects.annotate(num_answers=Count('user__answers')).order_by('-num_answers')[:5]

    page = paginate(questions, request, per_page=5)
    return render(request, 'hot_questions.html', {
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': popular_tags,
        'top_mentors': top_mentors
    })


def new(request):
    questions = Question.objects.order_by('-created_at')
    popular_tags = Tag.objects.annotate(num_questions=Count('questions')).order_by('-num_questions')[:5]
    top_mentors = UserProfile.objects.annotate(num_answers=Count('user__answers')).order_by('-num_answers')[:5]
    page = paginate(questions, request, per_page=5)
    return render(request, 'new_questions.html', {
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': popular_tags,
        'top_mentors': top_mentors
    })


def tag_questions(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.filter(tags=tag).order_by('-created_at')
    popular_tags = Tag.objects.annotate(num_questions=Count('questions')).order_by('-num_questions')[:5]
    top_mentors = UserProfile.objects.annotate(num_answers=Count('user__answers')).order_by('-num_answers')[:5]
    page = paginate(questions, request, per_page=5)
    return render(request, 'questions_by_tag.html', {
        'tag': tag,
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': popular_tags,
        'top_mentors': top_mentors
    })


def question(request, question_id):
    one_question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=one_question).order_by('-created_at')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = one_question
            answer.author = request.user
            answer.save()
            return redirect('question', question_id=question_id)
    else:
        form = AnswerForm()
    return render(request, 'post.html', {
        'question': one_question,
        'answers': answers,
        'form': form
    })


@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form})


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


@login_required
def profile_settings(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        avatar_url = request.POST.get('avatar_url')

        user.username = username
        user.email = email
        profile.bio = bio
        profile.avatar_url = avatar_url

        user.save()
        profile.save()
        return redirect('profile_settings')

    return render(request, 'profile_settings.html', {
        'user': user,
        'profile': profile
    })

def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    avatar_url = profile.avatar_url if profile.avatar_url else static('img/profile.png')
    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'avatar_url': avatar_url
    })


@login_required
def profile_current_user(request):
    return redirect('profile', username=request.user.username)