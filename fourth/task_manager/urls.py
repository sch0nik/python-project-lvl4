from django.urls import path

from fourth.task_manager import views

urlpatterns = [
    path('', views.index),
]
