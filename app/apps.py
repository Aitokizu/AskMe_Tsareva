from django.apps import AppConfig
from django.dispatch import receiver

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Импортируем сигналы и модели только после того, как приложение готово
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User
        from .models import UserProfile  # Используем UserProfile вместо Profile

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
                UserProfile.objects.create(user=instance)  # Используем UserProfile

        @receiver(post_save, sender=User)
        def save_user_profile(sender, instance, **kwargs):
            if hasattr(instance, 'userprofile'):  # Проверяем, существует ли профиль
                instance.userprofile.save()  # Используем userprofile