from django.contrib.auth.models import User
from django.db import models


class StatusTask(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200)
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='autor',
    )
    status = models.ForeignKey(
        StatusTask,
        on_delete=models.PROTECT,
        related_name='status',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
