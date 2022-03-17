from django.test import tag
from django.test import TestCase
from django.urls import reverse

from fourth.task_manager.models import User, Task, StatusTask, Label


class TestFilters(TestCase):
    fixtures = ['fixtures.json']

    def test_status(self):
        self.client.login(username='user1', password='123')

        pk = 3
        response = self.client.get(reverse('tasks'), {'status': pk})
        queryset = Task.objects.all().filter(status=pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    def test_label(self):
        self.client.login(username='user1', password='123')

        pk = 2
        response = self.client.get(reverse('tasks'), {'label': pk})
        queryset = Task.objects.all().filter(label=pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    def test_executor(self):
        self.client.login(username='user1', password='123')

        pk = 2
        response = self.client.get(reverse('tasks'), {'label': pk})
        queryset = Task.objects.all().filter(label=pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    def test_my_task(self):
        self.client.login(username='user1', password='123')
        pk = User.objects.get(username='user1').pk

        response = self.client.get(reverse('tasks'), {'my_task': 'on'})
        queryset = Task.objects.all().filter(autor=pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    def test_misc(self):
        self.client.login(username='user1', password='123')
        pk_user = User.objects.get(username='user2').pk
        pk_status = 2

        response = self.client.get(
            reverse('tasks'),
            {
                'autor': 'user2',
                'status': pk_status,
            }
        )
        queryset = Task.objects.all().filter(autor=pk_user).filter(status=pk_status)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)
