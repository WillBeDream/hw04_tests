from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator
    }
    return render(
        request,
        "index.html",
        context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "group": group,
        "page": page,
        "paginator": paginator
    }
    return render(
        request,
        "group.html",
        context)


def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == "GET" or not form.is_valid():
        context = {"form": form}
        return render(request, "new.html", context)
    post = form.save(commit=False)
    post.author = request.user
    form.save()
    return redirect("index")


def profile(request, username):
    author_posts = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author=author_posts).order_by('-pub_date').all()
    posts_count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "posts_count": posts_count,
        "paginator": paginator,
        "posts": posts,
        "author_posts": author_posts,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    author_posts = get_object_or_404(User, username=username)
    post_count = Post.objects.filter(author=author_posts).count()
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'author_posts': author_posts,
        'posts_count': post_count,
        'post': post,
    }
    return render(request, 'post.html', context)


def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    if request.user != author: 
        return redirect('post', username=username, post_id=post_id)

    form = PostForm(request.POST, instance=post)
    if request.method == 'GET' or not form.is_valid(): 
        return render(request, 
                      'post_new.html', 
                      {'form': PostForm(instance=post), 'post': post})
    form.save() 
    return redirect('post', username=username, post_id=post_id) 
         
    
    
    
