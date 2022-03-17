from django.test import TestCase
from django.urls import reverse

from fourth.task_manager.models import Task, Label, StatusTask, User


class TestTask(TestCase):
    fixtures = ['fixtures.json']

    def test_create_task(self):
        self.assertTrue(self.client.login(username='user2', password='123'))

        response = self.client.get(reverse('create_task'))
        self.assertTrue(response.status_code == 200)

        response = self.client.post(
            reverse('create_task'),
            {
                'name': 'test_task1',
                'description': 'text',
                'executor': User.objects.get(username='user1').pk,
                'status': StatusTask.objects.get(name='Разработка').pk,
                'label': Label.objects.get(name='Для всех').pk,
            }
        )
        self.assertTrue(Task.objects.get(name='test_task1'))

    def test_update_task(self):
        self.client.login(username='user1', password='123')
        task = Task.objects.get(pk=1)
        pk = task.pk

        self.client.post(
            reverse('update_task', args=[pk]),
            {
                'name': 'update_task',
                'description': task.description,
                'executor': task.executor.pk,
                'status': task.status.pk,
            }
        )

        self.assertTrue(Task.objects.get(pk=pk).name == 'update_task')

    def test_delete_task(self):
        self.client.login(username='user2', password='123')
        pk = Task.objects.get(pk=3).pk

        response = self.client.post(reverse('delete_task', args=[pk]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(pk=pk))
