from django.contrib import admin
from django.urls import include, path
from task_manager import views
from apps.user_app.views import LoginUserView, LogoutUserView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', include('apps.user_app.urls')),
    path('labels/', include('apps.label_app.urls')),
    path('statuses/', include('apps.status_app.urls')),
    path('tasks/', include('apps.task_app.urls')),
    path('admin/', admin.site.urls),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
