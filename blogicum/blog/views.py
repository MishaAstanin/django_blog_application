from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils.timezone import now
from django.http import Http404
from .models import Post, Category


def index(request):
    template_name = 'blog/index.html'
    post_list = Post.objects.select_related(
        'category', 'author', 'location').filter(
        Q(pub_date__lte=now()) 
        & Q(is_published=True) 
        & Q(category__is_published=True))[0:5]
    context = {'post_list': post_list}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    try:
        post = Post.objects.select_related(
            'category', 'author', 'location').get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404

    if (
        post.pub_date > now()
        or post.is_published is False
        or post.category.is_published is False
    ):
        raise Http404

    context = {
        'post': post
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404

    post_list = category.posts.select_related(
        'category', 'author', 'location').filter(
        Q(pub_date__lte=now()) & Q(is_published=True))
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template_name, context)
