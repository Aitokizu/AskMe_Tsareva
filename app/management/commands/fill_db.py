import random
from django.contrib.auth.models import User
from faker import Faker
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike
from django.core.management.base import BaseCommand
from django.db import transaction

import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from django.contrib.auth.models import User
from app.models import Tag, Question, Answer, QuestionLike, AnswerLike, UserProfile
from django.templatetags.static import static

fake = Faker()


class Command(BaseCommand):
    help = "Fill the database with test data"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio of entities to generate')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        self.stdout.write(f"Generating data with ratio: {ratio}")

        with transaction.atomic():
            self.generate_users(ratio)
            self.generate_tags(ratio)
            self.generate_questions(ratio * 10)
            self.generate_answers(ratio * 100)
            self.generate_likes(ratio * 200)

        self.stdout.write("Data generation complete.")

    def generate_users(self, count):
        self.stdout.write("Generating users...")
        default_avatar_url = static('img/profile.png')  # Дефолтный аватар
        for _ in range(count):
            username = fake.unique.user_name()
            email = fake.unique.email()
            user = User.objects.create_user(username=username, email=email, password='password123')
            # Создаем профиль для пользователя
            UserProfile.objects.create(user=user, avatar_url=default_avatar_url)
        self.stdout.write(f"Generated {count} users.")

    def generate_tags(self, count):
        self.stdout.write("Generating tags...")
        existing_tags = set(Tag.objects.values_list('name', flat=True))
        tags = []

        for _ in range(count):
            tag_name = fake.unique.word()
            while tag_name in existing_tags:
                tag_name = fake.unique.word()
            existing_tags.add(tag_name)
            tags.append(Tag(name=tag_name))

        Tag.objects.bulk_create(tags)
        self.stdout.write(f"Generated {count} tags.")

    def generate_questions(self, count):
        self.stdout.write("Generating questions...")
        users = list(User.objects.all())
        tags = list(Tag.objects.all())
        questions = []

        for _ in range(count):
            author = random.choice(users)
            title = fake.unique.sentence()
            text = fake.paragraph()
            question = Question(
                title=title,
                text=text,
                author=author
            )
            question.save()
            # Добавляем случайные теги
            question.tags.add(*random.sample(tags, k=min(3, len(tags))))
            questions.append(question)

        self.stdout.write(f"Generated {count} questions.")

    def generate_answers(self, count):
        self.stdout.write("Generating answers...")
        users = list(User.objects.all())
        questions = list(Question.objects.all())
        answers = []

        for _ in range(count):
            author = random.choice(users)
            question = random.choice(questions)
            text = fake.paragraph()
            answer = Answer(
                text=text,
                question=question,
                author=author
            )
            answers.append(answer)

        Answer.objects.bulk_create(answers)
        self.stdout.write(f"Generated {count} answers.")

    def generate_likes(self, count):
        self.stdout.write("Generating likes...")
        users = list(User.objects.all())
        questions = list(Question.objects.all())
        answers = list(Answer.objects.all())

        question_likes = []
        answer_likes = []

        for _ in range(count):
            user = random.choice(users)

            # Лайк на случайный вопрос
            question = random.choice(questions)
            # Проверяем, если лайк еще не поставлен для этого пользователя и вопроса
            if not QuestionLike.objects.filter(user=user, question=question).exists():
                question_likes.append(QuestionLike(user=user, question=question))

            # Лайк на случайный ответ
            answer = random.choice(answers)
            # Проверяем, если лайк еще не поставлен для этого пользователя и ответа
            if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                answer_likes.append(AnswerLike(user=user, answer=answer))

        # Используем bulk_create для добавления лайков в базу данных только если они уникальны
        if question_likes:
            QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)  # Игнорировать конфликты
        if answer_likes:
            AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)  # Игнорировать конфликты

        self.stdout.write(f"Generated {count} likes for questions and answers.")