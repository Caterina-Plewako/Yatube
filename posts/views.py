from datetime import datetime

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_page

from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator

from .models import Post, Group, User, Comment, Follow
from .forms import PostForm, CommentForm


@cache_page(20)
def index(request):
    latest = Post.objects.all()
    paginator = Paginator(latest, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page,
                                          'paginator': paginator})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    posts_number = posts.count()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'author': author, 'posts': posts,
                                            'page': page, 'paginator': paginator,
                                            'posts_number': posts_number})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.post = post
            item.save()
            return redirect('post', username=post.author, post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'post.html', {'form': form, 'author': post.author,
                                         'post_id': post_id, 'item': item})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=author, id=post_id)
    item = post.comments.all()

    posts = author.posts.all()
    posts_number = posts.count()
    form = CommentForm(request.POST)
    return render(request, 'post.html', {'author': author, 'post': post,
                                         'form': form,
                                         'posts_number': posts_number,
                                         'items': item})


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if author == user:
        if request.method == 'POST':
            form = PostForm(
                request.POST, files=request.FILES or None, instance=post)
            if form.is_valid():
                post.save()
        else:
            form = PostForm(instance=post)
            return render(request, 'new_post.html', {'form': form, 'post_id': post_id,
                                                     'author': author, 'post': post})
    return redirect('post', username=post.author, post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=request.user, author=author).exists()
    if author != request.user:
        if not follow:
            Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=request.user, author=author)
    if author != request.user:
        if follow.exists():
            follow.delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
