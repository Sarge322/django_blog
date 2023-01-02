from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddPostForm
from .models import *


def index(request):  # HttpRequest
    posts = Blog_theme.objects.all()

    context = {
        'posts': posts,
        'title': 'Главна страница',
        'cat_selected': 0,
        'menu_selected': 'about'
    }
    return render(request, 'blog_theme/index.html', context=context)


def about(request):
    return render(request, 'blog_theme/about.html', {'title': 'About'})


def python_fiddle(request, fid_id):
    print(request.GET)
    print(f"POST: {request.POST}")
    return HttpResponse(f"Песочница для кода питона {fid_id}")


def pageNotFound(request, exception):
    return HttpResponseNotFound("Page not found!!!")


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                Blog_theme.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста!!!')
    else:
        form = AddPostForm()
    return render(request, 'blog_theme/addpage.html', {'form': form, 'title': 'Add new post'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    post = get_object_or_404(Blog_theme, slug=post_slug)

    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post_slug,
    }

    return render(request, 'blog_theme/post.html', context=context)


def show_category(request, cat_slug):
    posts = Blog_theme.objects.filter(cat__slug=cat_slug)

    if len(posts) == 0:
        raise Http404()
    context = {
        'posts': posts,
        'title': 'Отображение по разделам',
        'cat_selected': cat_slug,
    }

    return render(request, 'blog_theme/index.html', context=context)














