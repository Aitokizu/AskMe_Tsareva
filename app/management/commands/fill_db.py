from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike
import random

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **kwargs):
        ratio = int(input("Enter ratio: "))


        users = []
        for i in range(ratio):
            user = User.objects.create_user(
                username=f"user{i}",
                password="password"
            )
            users.append(user)


        tags = []
        for i in range(ratio):
            tag = Tag.objects.create(name=f"tag{i}")
            tags.append(tag)


        questions = []
        for i in range(ratio * 10):
            question = Question.objects.create(
                title=f"Question {i}",
                text=f"This is the text of question {i}.",
                author=random.choice(users),
            )
            question.tags.set(random.sample(tags, random.randint(1, 5)))
            questions.append(question)

        # Создание ответов
        answers = []
        for i in range(ratio * 100):
            answer = Answer.objects.create(
                text=f"This is the text of answer {i}.",
                author=random.choice(users),
                question=random.choice(questions),
            )
            answers.append(answer)


        for i in range(ratio * 200):
            QuestionLike.objects.create(
                user=random.choice(users),
                question=random.choice(questions),
            )
            AnswerLike.objects.create(
                user=random.choice(users),
                answer=random.choice(answers),
            )

        self.stdout.write(self.style.SUCCESS("Database filled successfully!"))