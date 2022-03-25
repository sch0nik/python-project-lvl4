from django.test import TestCase
from django.urls import reverse

from apps.user_app.models import User


class TestUsers(TestCase):
    fixtures = ['fixtures.json']

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('delete_user')
        user.set_password('123')
        user.first_name = 'Del'
        user.last_name = 'Ete'
        user.save()

    def test_create_user(self):
        response = self.client.get(reverse('create'))
        self.assertTrue(response.status_code == 200)

        response = self.client.post(
            reverse('create'),
            {
                'username': 'test',
                'first_name': 'john',
                'last_name': 'smith',
                'password1': '123',
                'password2': '123',
            }
        )
        self.assertRedirects(response, '/login/')
        self.assertTrue(User.objects.get(username='test'))

    def test_update_user(self):
        user = User.objects.get(username='user1')
        pk = user.pk

        response = self.client.get(reverse('update', args=[pk]))
        self.assertTrue(response.status_code == 302)

        self.client.login(username='user1', password='123')
        response = self.client.post(
            reverse('update', args=[pk]),
            data={
                'username': 'test',
                'first_name': 'john',
                'last_name': 'smith',
                'password1': '123',
                'password2': '123',
            }
        )
        self.assertRedirects(response, '/users/')
        self.assertTrue(User.objects.get(username='test'))
        self.assertTrue(User.objects.get(username='test').pk == pk)

    def test_delete_user(self):
        user = User.objects.get(username='delete_user')
        pk = user.pk

        response = self.client.get(reverse('delete', args=[pk]))
        self.assertTrue(response.status_code == 302)

        self.client.login(username='delete_user', password='123')
        response = self.client.post(reverse('delete', args=[pk]))
        self.assertRedirects(response, '/users/')
        self.assertFalse(User.objects.filter(pk=pk))

    def test_page_users(self):
        response = self.client.get(reverse('users'))
        self.assertTrue(response.status_code == 200)
