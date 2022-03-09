from django.urls import path

from fourth.task_manager import views


urlpatterns = [
    # Users
    path('', views.IndexView.as_view(), name='index'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('users/<int:pk>/update/', views.UpdateUserView.as_view(), name='update'),
    path('users/<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),

    # Status
    path('statuses/', views.StatusesView.as_view(), name='statuses'),
    path('statuses/create', views.CreateStatusView.as_view(), name='create_status'),
    path('statuses/<int:pk>/update', views.UpdateStatusView.as_view(), name='update_status'),
    path('statuses/<int:pk>/delete', views.DeleteStatusView.as_view(), name='delete_status'),

    # Task
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('tasks/create', views.CreateTaskView.as_view(), name='create_task'),
    path('tasks/<int:pk>/update', views.UpdateTaskView.as_view(), name='update_task'),
    path('tasks/<int:pk>/delete', views.DeleteTaskView.as_view(), name='delete_task'),
    path('tasks/<int:pk>/', views.TaskView.as_view(), name='task'),

]
