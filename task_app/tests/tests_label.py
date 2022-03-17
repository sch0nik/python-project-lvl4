from django.test import TestCase
from django.urls import reverse

from task_app.models import Label


class TestLabels(TestCase):
    fixtures = ['fixtures.json']

    @classmethod
    def setUpTestData(cls):
        label = Label()
        label.name = 'delete_label'
        label.save()

    def test_create_label(self):
        self.client.login(username='user1', password='123')

        response = self.client.get(reverse('create_label'))
        self.assertTrue(response.status_code == 200)

        response = self.client.post(
            reverse('create_label'),
            {'name': 'test1'},
        )

        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.get(name='test1'))

    def test_update_label(self):
        self.client.login(username='user1', password='123')

        pk = Label.objects.get(pk=1).pk

        response = self.client.post(
            reverse('update_label', args=[pk]),
            data={'name': 'test_test'}
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.get(name='test_test'))
        self.assertTrue(Label.objects.get(name='test_test').pk == pk)

    def test_delete_label(self):
        self.client.login(username='user1', password='123')

        pk = Label.objects.get(name='delete_label').pk

        response = self.client.post(reverse('delete_label', args=[pk]))
        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Label.objects.filter(pk=pk))
