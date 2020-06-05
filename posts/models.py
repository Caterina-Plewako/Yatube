from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(verbose_name='Группа', max_length=200)
    slug = models.SlugField(unique=True, max_length=50)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.title}, {self.id}'


class Post(models.Model):
    text = models.TextField(verbose_name='Текст', blank=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_posts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              verbose_name='Группа', blank=True,
                              null=True, related_name='group_posts')
    image = models.ImageField(
        upload_to='posts/', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True,
                             null=True, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_comments')
    text = models.TextField(verbose_name='Комментарий', blank=False)
    created = models.DateTimeField('date published', auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    def __str__(self):
        return f'{self.user}, {self.author}'
