from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.core.exceptions import ValidationError

# Create your models here.


def validate_image(file):
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
    if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
        raise ValidationError('Uploaded file is not a valid image.')

def validate_file_size(file):
    max_size_kb = 500  # Максимальный размер в КБ
    if file.size > max_size_kb * 1024:
        raise ValidationError(f'File size exceeds {max_size_kb} KB.')

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True, validators=[validate_image, validate_file_size])

    def str(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def str(self):
        return self.name

class QuestionManager(models.Manager):
    def best(self):
        return self.annotate(likes_count=Count('likes')).order_by('-likes_count', '-created_at')

    def newest(self):
        return self.order_by('-created_at')

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

class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Answer to {self.question.title} by {self.author.username}"

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'question')

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'answer')

