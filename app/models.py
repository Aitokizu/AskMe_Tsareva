from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=10)
    joined_at = models.DateTimeField(auto_now_add=True)
    bio = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Tag(models.Model):
    name = models.CharField(max_length=255)

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    add_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Rating(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)