from django.test import TestCase, tag
from django.urls import reverse

from task_app.models import StatusTask, Task


class TestStatus(TestCase):
    fixtures = ['fixtures.json']

    @classmethod
    def setUpTestData(cls):
        status = StatusTask()
        status.name = 'delete_status'
        status.save()

    def test_create_status(self):
        self.client.login(username='user1', password='123')

        response = self.client.get(reverse('create_status'))
        self.assertTrue(response.status_code == 200)

        response = self.client.post(reverse('create_status'), {'name': 'test1'})
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(StatusTask.objects.get(name='test1'))
        response = self.client.get(reverse('statuses'))
        self.assertIn(b'test1', response.content)

    def test_update_status(self):
        self.client.login(username='user1', password='123')

        pk = StatusTask.objects.get(pk=1).pk

        response = self.client.post(
            reverse('update_status', args=[pk]),
            data={'name': 'test_test'}
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(StatusTask.objects.get(name='test_test'))
        self.assertTrue(StatusTask.objects.get(name='test_test').pk == pk)

    def test_delete_status(self):
        self.client.login(username='user1', password='123')

        pk = StatusTask.objects.get(pk=1).pk

        response = self.client.post(reverse('delete_status', args=[pk]))
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(StatusTask.objects.filter(pk=pk))

    def test_status(self):
        self.client.login(username='user1', password='123')

        pk = 3
        response = self.client.get(reverse('tasks'), {'status': pk})
        queryset = Task.objects.all().filter(status=pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)