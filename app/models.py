from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.core.exceptions import ValidationError


# Валидация изображений
def validate_image(file):
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
    if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
        raise ValidationError('Uploaded file is not a valid image.')

def validate_file_size(file):
    max_size_kb = 500  # Максимальный размер в КБ
    if file.size > max_size_kb * 1024:
        raise ValidationError(f'File size exceeds {max_size_kb} KB.')


# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.FileField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[validate_image, validate_file_size]
    )

    def str(self):
        return self.user.username


# Теги
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def str(self):
        return self.name


# Менеджер для вопросов
class QuestionManager(models.Manager):
    def best(self):
        return self.annotate(likes_count=Count('likes')).order_by('-likes_count', '-created_at')

    def newest(self):
        return self.order_by('-created_at')


# Вопросы
class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def str(self):
        return self.title

    def get_absolute_url(self):
        return f"/question/{self.id}/"


# Ответы
class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Answer to {self.question.title} by {self.author.username}"


# Лайки к вопросам
class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'question')

    def str(self):
        return f"{self.user.username} likes {self.question.title}"


# Лайки к ответам
class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'answer')

    def str(self):
        return f"{self.user.username} likes an answer to {self.answer.question.title}"