from django import forms
from .models import Question, Answer, User
from django.core.exceptions import ValidationError

# Форма для создания нового вопроса
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    # Дополнительная валидация для поля 'title'
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError("Title must be at least 10 characters.")
        return title

# Форма для добавления нового ответа
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    # Дополнительная валидация для поля 'text'
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise ValidationError("Answer must be at least 10 characters.")
        return text

# Форма для регистрации нового пользователя
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    # Валидация пароля
    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise ValidationError("Passwords do not match.")
        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user