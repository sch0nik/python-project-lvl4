from django.urls import path

from apps.task_app import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='tasks'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/update/', views.UpdateTaskView.as_view(), name='update_task'),
    path('<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete_task'),
    path('<int:pk>/', views.TaskView.as_view(), name='task'),
]
