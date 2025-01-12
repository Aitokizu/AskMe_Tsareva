from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Question, Answer, UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError("Title must be at least 10 characters.")
        return title

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise ValidationError("Answer must be at least 10 characters.")
        return text