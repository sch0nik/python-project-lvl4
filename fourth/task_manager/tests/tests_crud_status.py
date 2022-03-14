from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from fourth.task_manager.models import StatusTask


class TestCRUDStatus(TestCase):

    def setUp(self):
        StatusTask.objects.create(name='test')

        user = User.objects.create_user(username='user', password='123')
        user.first_name = 'Юзер'
        user.last_name = 'Юзеров'
        user.save()

        self.client.force_login(user)

    def test_create_status(self):
        response = self.client.post(reverse('create_status'), {'name': 'test1'})
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(StatusTask.objects.get(name='test1'))

    def test_update_status(self):
        pk = StatusTask.objects.get(name='test').pk
        response = self.client.post(
            reverse('update_status', args=[pk]),
            data={'name': 'test_test'}
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(StatusTask.objects.get(name='test_test'))
        self.assertTrue(StatusTask.objects.get(name='test_test').pk == pk)

    def test_delete_status(self):
        pk = StatusTask.objects.get(name='test').pk
        response = self.client.post(reverse('delete_status', args=[pk]))
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(StatusTask.objects.filter(pk=pk))
