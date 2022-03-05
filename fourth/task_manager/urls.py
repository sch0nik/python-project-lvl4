from django.urls import path

from fourth.task_manager import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('users/<int:pk>/update/', views.UpdateUserView.as_view(), name='update'),
    path('users/<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]
