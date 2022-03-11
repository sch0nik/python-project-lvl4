from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusTask(models.Model):
    name = models.CharField(_('Имя'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(_('Имя'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(_('Имя'), max_length=100, unique=True)
    description = models.TextField(_('Описание'), max_length=200)
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='task',
    )
    status = models.ForeignKey(
        StatusTask,
        on_delete=models.PROTECT,
        related_name='task',
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    autor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authorship',
    )

    label = models.ManyToManyField(Label, blank=True, related_name='task')

    def __str__(self):
        return self.name
