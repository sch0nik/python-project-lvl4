from django.urls import path

from apps.user_app import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateUserView.as_view(success_url='/users/'), name='update',),
    path('<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete'),
]
