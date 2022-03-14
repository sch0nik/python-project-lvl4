from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from fourth.task_manager.models import Label


class TestCRUDLabel(TestCase):

    def setUp(self):
        Label.objects.create(name='test')

        user = User.objects.create_user(username='user', password='123')
        user.first_name = 'Юзер'
        user.last_name = 'Юзеров'
        user.save()

        self.client.force_login(user)

    def test_create_label(self):
        response = self.client.post(reverse('create_label'), {'name': 'test1'})
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.get(name='test1'))

    def test_update_label(self):
        pk = Label.objects.get(name='test').pk
        response = self.client.post(
            reverse('update_label', args=[pk]),
            data={'name': 'test_test'}
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.get(name='test_test'))
        self.assertTrue(Label.objects.get(name='test_test').pk == pk)

    def test_delete_label(self):
        pk = Label.objects.get(name='test').pk
        response = self.client.post(reverse('delete_label', args=[pk]))
        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Label.objects.filter(pk=pk))
