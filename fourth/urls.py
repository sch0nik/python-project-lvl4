from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('fourth.task_manager.urls')),
    path('admin/', admin.site.urls),
]
