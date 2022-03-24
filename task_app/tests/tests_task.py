from django.test import TestCase
from django.urls import reverse

from task_app.models import Task, Label, StatusTask, User


class TestTask(TestCase):
    fixtures = ['fixtures.json']
    delete_task = None

    @classmethod
    def setUpTestData(cls):
        user = User.objects.all()[0]
        status = StatusTask.objects.all()[0]
        label = Label.objects.all()[0]
        task = Task()
        task.name = 'delete_task'
        task.description = 'text'
        task.executor = user
        task.autor = user
        task.status = status
        task.save()
        task.labels.set([label])
        task.save()
        cls.delete_task = task

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
                'labels': Label.objects.get(name='Для всех').pk,
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
        user = self.delete_task.autor
        self.client.login(username=user.username, password='123')
        pk = self.delete_task.pk

        response = self.client.post(reverse('delete_task', args=[pk]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(pk=pk))

    def test_executor(self):
        self.client.login(username='user1', password='123')

        pk = 2
        response = self.client.get(reverse('tasks'), {'labels': pk})
        queryset = Task.objects.all().filter(labels=pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)

    def test_my_task(self):
        self.client.login(username='user1', password='123')
        pk = User.objects.get(username='user1').pk

        response = self.client.get(reverse('tasks'), {'my_task': 'on'})
        queryset = Task.objects.all().filter(autor=pk)
        value = response.context['task_list']
        self.assertQuerysetEqual(queryset, value, ordered=False)
