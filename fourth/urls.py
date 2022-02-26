from django.contrib import admin
from django.urls import path

from fourth.task_manager import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/create/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('users/<int:pk>/update/', views.UpdateView.as_view(), name='update'),
    path('users/<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
