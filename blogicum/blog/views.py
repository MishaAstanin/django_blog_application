from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils.timezone import now
from django.http import Http404
from .models import Post, Category


def filter_posts(posts):
    return posts.filter(
        Q(pub_date__lte=now())
        & Q(is_published=True)
        & Q(category__is_published=True)
    )


def index(request):
    template_name = 'blog/index.html'
    post_list = filter_posts(
        Post.objects.select_related('category', 'author', 'location')
    )[0:5]
    context = {'post_list': post_list}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        filter_posts(
            Post.objects.select_related('category', 'author', 'location')
        ),
        pk=post_id
    )
    context = {
        'post': post
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    post_list = filter_posts(
        category.posts.select_related('category', 'author', 'location')
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template_name, context)
