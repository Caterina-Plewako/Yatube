from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Post, Follow, Comment


class TestStringMethods(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='alice', email='mynameis@alice.ru', password='12345'
        )
        self.text = Post.objects.create(
            text='Follow the white rabbit.', author=self.user)

    def test_profile_exist(self):
        response = self.client.get(f'/{self.user.username}')
        self.assertEqual(response.status_code, 200)

    def test_new(self):
        response = self.client.get('/new')
        self.assertEqual(response.status_code, 302)

    def test_redirect_not_logged_user(self):
        self.client.logout()
        response = self.client.get('/new', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/new')

    def test_post_exist(self):
        response = self.client.get('')
        self.assertContains(
            response, self.text,
            msg_prefix='Новый пост не появляется на главной странице')
        response = self.client.get(f'/{self.user.username}')
        self.assertContains(
            response, self.text,
            msg_prefix='Новый пост не появляется в профайле пользователя')
        response = self.client.get(
            f'/{self.user.username}/{self.text.id}/')
        self.assertContains(
            response, self.text,
            msg_prefix='Новый пост не появляется на странице просмотра записи')

    def test_author_can_edit(self):
        self.client.post(f'/{self.user.username}/{self.text.id}/edit/',
                         {'text': 'edited'})
        response = self.client.get('')
        self.assertContains(
            response, self.text,
            msg_prefix='Отредактированный пост не появляется на главной странице')
        response = self.client.get(f'/{self.user.username}')
        self.assertContains(
            response, self.text,
            msg_prefix='Отредактированный пост не появляется в профайле пользователя')
        response = self.client.get(f'/{self.user.username}/{self.text.id}/')
        self.assertContains(
            response, self.text,
            msg_prefix='Отредактированный пост не появляется на странице просмотра записи')

    def test_404(self):
        response = self.client.get('some/url/404')
        self.assertEqual(response.status_code, 404)
