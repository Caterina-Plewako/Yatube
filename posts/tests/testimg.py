from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

import tempfile
from PIL import Image

from .models import Post, Group


class TestImg(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='alice', email='mynameis@alice.ru', password='12345'
        )
        self.client.force_login(self.user)
        self.group = Group.objects.create(title='group', slug='noname')
        self.post = Post.objects.create(
            text='Follow the white rabbit.', author=self.user, group=self.group)

    def test_page_with_img(self):
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')
        with open(f.name, mode='rb') as img:
            self.client.post(reverse('post_edit', kwargs={
                'username': self.user.username, 'post_id': self.post.id}),
                {'text': 'Image', 'image': img, 'group': self.group.id})
        tag = 'img class="card-img" src="/media/'
        response = self.client.get('')
        self.assertContains(response, tag,
                            msg_prefix='Тэг <img> не найден на главной странице')
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(response, tag,
                            msg_prefix='Тэг <img> не найден в профайле пользователя')
        response = self.client.get(
            reverse('post', kwargs={'username': self.user.username,
                                    'post_id': self.post.id}))
        self.assertContains(response, tag,
                            msg_prefix='Тэг <img> не найден на странице просмотра поста')
        response = self.client.get(
            reverse('group', kwargs={'slug': self.post.group.slug}))
        self.assertContains(response, tag,
                            msg_prefix='Тэг <img> не найден на странице группы')

    def test_not_img(self):
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b'Test text')
        with open(f.name, mode='rb') as not_img:
            response = self.client.post(reverse('post_edit', kwargs={
                'username': self.user.username, 'post_id': self.post.id}),
                {'text': 'Not image', 'image': not_img}, follow=True)
        self.assertIn('image', response.context['form'].errors)
