from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.label_app.models import Label
from apps.status_app.models import StatusTask
from apps.user_app.models import User


class Task(models.Model):
    name = models.CharField(_('Имя'), max_length=100, unique=True)
    description = models.TextField(_('Описание'), max_length=200)
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='task',
        verbose_name=_('Исполнитель'),
    )
    status = models.ForeignKey(
        StatusTask,
        on_delete=models.PROTECT,
        related_name='task',
        verbose_name=_('Статус'),
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    autor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authorship',
        verbose_name=_('Автор'),
    )

    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='task',
        verbose_name=_('Метки'),
    )

    def __str__(self):
        return self.name
