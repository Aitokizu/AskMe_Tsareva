from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from .forms import QuestionForm, AnswerForm, ProfileForm
from .models import Question, Answer, UserProfile, Tag
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Question, QuestionLike



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


from django.db.models import Count
from .models import Question, Tag, UserProfile

def index(request):
    questions = Question.objects.annotate(
        likes_count=Count('likes'),  # Аннотируем количество лайков
        answers_count=Count('answers')  # Аннотируем количество ответов
    ).order_by('-likes_count')  # Сортируем по количеству лайков

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
    questions = Question.objects.annotate(
        likes_count=Count('likes'),  # Аннотируем количество лайков
        answers_count=Count('answers')  # Аннотируем количество ответов
    ).order_by('-created_at')  # Сортируем по дате создания

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
    one_question = get_object_or_404(
        Question.objects.annotate(
            likes_count=Count('likes'),  # Аннотируем количество лайков
            answers_count=Count('answers')  # Аннотируем количество ответов
        ),
        id=question_id
    )

    answers = Answer.objects.filter(question=one_question).annotate(
        likes_count=Count('likes')  # Аннотируем количество лайков для ответов
    ).order_by('-created_at')

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
            form.save_m2m()  # Сохраняем теги
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
    profile, created = UserProfile.objects.get_or_create(user=user)  # Создаем профиль, если его нет

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_settings')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_settings.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)

    avatar_url = profile.avatar.url if profile.avatar else static('img/profile.png')

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'avatar_url': avatar_url
    })


@login_required
def profile_current_user(request):
    return redirect('profile', username=request.user.username)


@require_POST
@login_required
def like_question(request):
    question_id = request.POST.get('question_id')
    action = request.POST.get('action')
    question = get_object_or_404(Question, id=question_id)

    if action == 'like':
        like, created = QuestionLike.objects.get_or_create(user=request.user, question=question)
        if not created:
            return JsonResponse({'status': 'error', 'message': 'You already liked this question.'})
    elif action == 'dislike':
        like = QuestionLike.objects.filter(user=request.user, question=question).first()
        if like:
            like.delete()
        else:
            return JsonResponse({'status': 'error', 'message': 'You have not liked this question yet.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid action.'})

    likes_count = question.likes.count()
    return JsonResponse({'status': 'ok', 'likes_count': likes_count})

@require_POST
@login_required
def mark_correct_answer(request):
    question_id = request.POST.get('question_id')
    answer_id = request.POST.get('answer_id')
    question = get_object_or_404(Question, id=question_id)
    answer = get_object_or_404(Answer, id=answer_id)

    if question.author != request.user:
        return JsonResponse({'status': 'error', 'message': 'Only the author can mark correct answers.'})

    question.correct_answer = answer
    question.save()
    return JsonResponse({'status': 'ok'})