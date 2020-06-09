from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Post


class TestCache(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='alice', email='mynameis@alice.ru', password='12345'
        )
        self.client.force_login(self.user)
        self.text = Post.objects.create(
            text='Follow the white rabbit.', author=self.user)

    def test_cache(self):
        response = self.client.get('')
        html1 = response.content.decode('utf-8')
        self.client.post(reverse('new_post'), {
                         'text': 'Interesting text'}, follow=True)
        response = self.client.get('')
        html2 = response.content.decode('utf-8')
        self.assertHTMLEqual(html1, html2)
