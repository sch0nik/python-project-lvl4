from django.contrib.auth.models import User
from django.test import Client, TestCase


class TestRout(TestCase):
    test_username = 'username'
    test_first_name = 'first_name'
    test_last_name = 'last_name'
    test_pass = 'password'

    @classmethod
    def setUpTestData(cls):
        """Тестовый юзер."""
        user = User.objects.create_user(
            username=cls.test_username,
            password=cls.test_pass,
        )
        user.first_name = cls.test_first_name
        user.last_name = cls.test_last_name
        user.save()

    def test_login_get(self):
        """Страница входа."""
        client = Client()
        response = client.get('/login/')
        self.assertTemplateUsed(
            template_name='base_login.html',
            response=response,
        )

    def test_login_post(self):
        """Вход пользователя и редирект на главную страницу."""
        client = Client()
        response = client.post(
            '/login/',
            {'username': self.test_username, 'password': self.test_pass}
        )
        self.assertRedirects(expected_url='/', response=response)

    def test_logout_post(self):
        """Выход пользователя и редирект на главную страницу."""
        client = Client()
        response = client.post(
            '/login/',
            {'username': self.test_username, 'password': self.test_pass}
        )
        response = client.post(
            '/logout/',
        )
        self.assertRedirects(expected_url='/', response=response)

    def test_users_get(self):
        pass

    def test_user_create_get(self):
        pass

    def test_user_create_post(self):
        pass

    def test_user_update_post(self):
        pass

    def test_user_update_get(self):
        pass

    def test_user_delete_get(self):
        pass

    def test_user_delete_post(self):
        pass
