from django.test import TestCase, tag
from django.urls import reverse

from apps.label_app.models import Label
from apps.status_app.models import StatusTask
from apps.task_app.models import Task
from apps.user_app.models import User


class TestFilters(TestCase):
    fixtures = ['fixtures.json']

    def test_status_executor(self):
        username = 'user2'
        status_name = 'Разработка'
        self.client.login(username='user1', password='123')

        user = User.objects.get(username=username)
        status = StatusTask.objects.get(name=status_name)

        response = self.client.get(
            reverse('tasks'),
            {
                'executor': user.pk,
                'status': status.pk,
            }
        )
        queryset = Task.objects.filter(executor=user.pk).filter(status=status.pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    def test_status_label(self):
        self.client.login(username='user1', password='123')
        status_name = 'Разработка'
        label_name = 'Лидам'

        status = StatusTask.objects.get(name=status_name)
        label = Label.objects.get(name=label_name)
        queryset = Task.objects.filter(status=status.pk).filter(labels=label.pk)

        response = self.client.get(
            reverse('tasks'),
            data={
                'status': status.pk,
                'labels': label.pk,
            }
        )
        value = response.context['object_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    @tag('current')
    def test_executor_label(self):
        executor_name = 'user2'
        label_name = 'Лидам'

        self.client.login(username='user1', password='123')
        executor = User.objects.get(username=executor_name)
        label = Label.objects.get(name=label_name)

        response = self.client.get(
            reverse('tasks'),
            {
                'executor': executor.pk,
                'labels': label.pk,
            }
        )
        queryset = Task.objects.filter(executor=executor.pk).filter(labels=label.pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    def test_status_executor_my_task(self):
        username = 'user3'
        executor_name = 'user4'
        status_name = 'В работе'
        my_task = 'on'
        self.client.login(username=username, password='123')

        autor = User.objects.get(username=username)
        executor = User.objects.get(username=executor_name)
        status = StatusTask.objects.get(name=status_name)

        response = self.client.get(
            reverse('tasks'),
            {
                'executor': executor.pk,
                'status': status.pk,
                'my_task': my_task,
            }
        )
        queryset = Task.objects.filter(autor=autor.pk)
        queryset = queryset.filter(executor=executor.pk).filter(status=status.pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    def test_status_label_my_task(self):
        username = 'user6'
        status_name = 'В работе'
        label_name = 'Для всех'
        my_task = 'on'
        self.client.login(username=username, password='123')

        autor = User.objects.get(username=username)
        status = StatusTask.objects.get(name=status_name)
        label = Label.objects.get(name=label_name)

        response = self.client.get(
            reverse('tasks'),
            {
                'status': status.pk,
                'labels': label.pk,
                'my_task': my_task,
            }
        )
        queryset = Task.objects.filter(autor=autor.pk)
        queryset = queryset.filter(labels=label.pk).filter(status=status.pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    def test_executor_label_my_task(self):
        username = 'user2'
        executor_name = 'user5'
        label_name = 'Для всех'
        my_task = 'on'
        self.client.login(username=username, password='123')

        autor = User.objects.get(username=username)
        executor = User.objects.get(username=executor_name)
        label = Label.objects.get(name=label_name)

        response = self.client.get(
            reverse('tasks'),
            {
                'executor': executor.pk,
                'labels': label.pk,
                'my_task': my_task,
            }
        )
        queryset = Task.objects.filter(autor=autor.pk)
        queryset = queryset.filter(labels=label.pk).filter(executor=executor.pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)
