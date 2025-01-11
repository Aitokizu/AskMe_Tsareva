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
from app import views
from app.views import tag_questions

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('question/<int:question_id>', views.question, name='one_question'),
    path('ask/', views.ask, name='ask'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/', views.profile, name='profile'),
    path('tag/<str:tag_name>/', tag_questions, name='tag_questions'),
    path('admin/', admin.site.urls),
]
