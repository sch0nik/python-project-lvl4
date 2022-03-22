from django.urls import path

from task_app import views

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),

    # Users
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/create/', views.CreateUserView.as_view(), name='create'),
    path(
        'users/<int:pk>/update/',
        views.UpdateUserView.as_view(success_url='/users/'),
        name='update',
    ),
    path('users/<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete'),

    # Status
    path('statuses/', views.StatusesView.as_view(), name='statuses'),
    path('statuses/create/', views.CreateStatusView.as_view(), name='create_status'),
    path('statuses/<int:pk>/update/', views.UpdateStatusView.as_view(), name='update_status'),
    path('statuses/<int:pk>/delete/', views.DeleteStatusView.as_view(), name='delete_status'),

    # Task
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('tasks/create/', views.CreateTaskView.as_view(), name='create_task'),
    path('tasks/<int:pk>/update/', views.UpdateTaskView.as_view(), name='update_task'),
    path('tasks/<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete_task'),
    path('tasks/<int:pk>/', views.TaskView.as_view(), name='task'),

    # Label
    path('labels/', views.LabelsView.as_view(), name='labels'),
    path('labels/create/', views.CreateLabelView.as_view(), name='create_label'),
    path('labels/<int:pk>/update/', views.UpdateLabelView.as_view(), name='update_label'),
    path('labels/<int:pk>/delete/', views.DeleteLabelView.as_view(), name='delete_label'),

]
