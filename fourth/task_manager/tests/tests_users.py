from django.test import Client, TestCase

from fourth.task_manager.models import User


class TestCRUDUser(TestCase):
    # fixtures = 'users.json'

    def setUp(self):
        user = User.objects.create_user(username='user_semen', password='123')
        user.first_name = 'Семен'
        user.last_name = 'Слепаков'
        user.save()

        user = User.objects.create_user(username='user', password='123')
        user.first_name = 'Юзер'
        user.last_name = 'Юзеров'
        user.save()

    def test_create_user(self):
        response = self.client.post(
            '/users/create/',
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
        user = User.objects.get(username='user_semen')
        pk = user.pk
        self.client.login(username='user_semen', password='123')
        response = self.client.post(
            f'/users/{pk}/update/',
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
        user = User.objects.get(username='user')
        pk = user.pk
        self.client.login(username='user_semen', password='123')
        response = self.client.post(f'/users/{pk}/delete/')
        self.assertRedirects(response, '/users/')
        self.assertFalse(User.objects.filter(pk=pk))
