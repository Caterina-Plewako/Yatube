from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

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
        with open('media/posts/5-3.jpg', 'rb') as img:
            self.client.post(f'/{self.user.username}/{self.post.id}/edit/',
                             {'text': 'Image', 'group': self.group.id,
                              'image': img}, follow=True)

    def test_page_with_img(self):
        tag = 'img class="card-img" src="/media/'
        response = self.client.get('')
        self.assertContains(response, tag,
                            msg_prefix='Тэг <img> не найден на главной странице')
        response = self.client.get(f'/{self.user.username}')
        self.assertContains(response, tag,
                            msg_prefix='Тэг <img> не найден в профайле пользователя')
        response = self.client.get(f'/{self.user.username}/{self.post.id}/')
        self.assertContains(response, tag,
                            msg_prefix='Тэг <img> не найден на странице просмотра поста')
        response = self.client.get(f'/group/{self.post.group.slug}/')
        self.assertContains(response, tag,
                            msg_prefix='Тэг <img> не найден на странице группы')

    def test_not_img(self):
        with open('media/posts/some_text.docx', 'rb') as img:
            response = self.client.post(f'/{self.user.username}/{self.post.id}/edit/',
                                        {'text': 'Image', 'image': img}, follow=True)
        self.assertIn('image', response.context['form'].errors)
