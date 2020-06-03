from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Post, Follow, Comment


class TestFollow(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='alice', email='mynameis@alice.ru', password='12345'
        )
        self.client.force_login(self.user1)
        self.user2 = User.objects.create_user(
            username='user', email='user@net.ru', password='12345'
        )
        self.text = Post.objects.create(
            text='Interesting text', author=self.user2)

    def test_follow_unfollow(self):
        follow = Follow.objects.filter(
            user=self.user1, author=self.user2).exists()
        self.assertFalse(follow)
        follow = Follow.objects.create(user=self.user1, author=self.user2)
        self.assertTrue(follow)
        response = self.client.get(f'/{self.user2.username}')
        self.assertEqual(response.status_code, 200)

    def test_follow_list(self):
        self.post = Post.objects.create(
            text='Another interesting text', author=self.user2)
        response = self.client.get('/follow', follow=True)
        self.assertNotContains(
            response, self.post,
            msg_prefix='Новый пост появился у неподпианного пользователя')
        Follow.objects.create(user=self.user1, author=self.user2)
        response = self.client.get('/follow', follow=True)
        self.assertContains(
            response, self.post,
            msg_prefix='Новый пост не появился у подписчика')

    def test_comment(self):
        self.comment = self.client.post(
            f'/{self.user2.username}/{self.text.id}/comment/',
            {'text': 'Comment', 'author': self.user1})
        self.comment = Comment.objects.get(id=1)
        self.assertEqual(self.comment.text, 'Comment')
        self.client.logout()
        self.comment = self.client.post(
            f'/{self.user2.username}/{self.text.id}/comment/',
            {'text': 'Comment 2', 'author': self.user1})
        self.comment = Comment.objects.get(id=1)
        self.assertNotEqual(self.comment.text, 'Comment 2')
