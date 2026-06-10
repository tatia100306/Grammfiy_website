from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('grammar/', views.grammar_view, name='grammar'),
    path('chat/', views.chat_view, name='chat'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('progress/', views.progress_view, name='progress'),
]