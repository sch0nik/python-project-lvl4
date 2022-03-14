from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from fourth.task_manager.models import Task, Label, StatusTask


class TestCRUDTask(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='user', password='123')
        user.first_name = 'Юзер'
        user.last_name = 'Юзеров'
        user.save()

        label = Label.objects.create(name='label')
        status = StatusTask.objects.create(name='status')

        task = Task.objects.create(name='test_task')
        task.description = 'test text test text test text test text'
        # task.executor = user
        task.autor = user
        task.status = status
        task.label = label
        task.save()

        self.client.force_login(user)

    # def test_create_task(self):
    #     response = self.client.post(
    #         reverse('create_task'),
    #         {
    #             'name': 'test_task1',
    #             'description': 'text',
    #             'executor': 'smith',
    #             'autor': '123',
    #             'status': '123',
    #             'label': '123',
    #         }
    #     )
    #     self.assertRedirects(response, '/login/')
    #     self.assertTrue(Task.objects.get(username='test'))

    def test_update_task(self):
        pk = Task.objects.get(name='test_task').pk
        response = self.client.post(
            reverse('update_task', args=[pk]),
            data={
                'name': 'edit_test',
            }
        )
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.get(username='edit_test'))
        self.assertTrue(Task.objects.get(username='edit_test').pk == pk)

    def test_delete_task(self):
        pk = Task.objects.get(name='test').pk
        response = self.client.post(reverse('delete_task', args=[pk]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(pk=pk))
