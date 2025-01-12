"""
URL configuration for askme_tsareva project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from app import views
from django.conf import settings
from django.conf.urls.static import static

from app.views import like_question, mark_correct_answer

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('question/<int:question_id>/', views.question, name='one_question'),
    path('ask/', views.ask, name='ask'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/', views.profile_current_user, name='profile_current_user'),
    path('accounts/profile/', RedirectView.as_view(pattern_name='profile_current_user')),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('tag/<str:tag_name>/', views.tag_questions, name='tag_questions'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('like/', like_question, name='like_question'),
    path('mark_correct/', mark_correct_answer, name='mark_correct_answer'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)