from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddPostForm
from .models import *


# def index(request):  # HttpRequest
#     posts = Blog_theme.objects.all()
#
#     context = {
#         'posts': posts,
#         'title': 'Главна страница',
#         'cat_selected': 0,
#         'menu_selected': 'about'
#     }
#     return render(request, 'blog_theme/index.html', context=context)

# создаем класс главной страницы
class BlogHome(ListView):
    # атрибут model ссылается на модель Blog_theme, создается список всех записей модели Blog_theme
    model = Blog_theme
    # прописываем путь нашей страницы
    template_name = 'blog_theme/index.html'
    # передаем список в виде переменной, указаной в шаблоне index.html(posts), object_list - дефолтная переменная
    context_object_name = 'posts'

    # создаем функцию для динамического и стат. контекста
    def get_context_data(self, *, object_list=None, **kwargs):
        # обращаемся к базовому классу ListView и берем существующий контекст, чтобы не создать новый пустой и все затереть
        context = super().get_context_data(**kwargs)
        # меняем атрибут контекста title, отображение имени вкладки
        context['title'] = 'Главная страница'
        # передаем дефолтный указатель выбранной категории
        context['cat_selected'] = 0
        return context

    # фильтруем только опубликованные статьи (с галкой is_published)
    def get_queryset(self):
        return Blog_theme.objects.filter(is_published=True)


def about(request):
    return render(request, 'blog_theme/about.html', {'title': 'About'})


def python_fiddle(request, fid_id):
    return HttpResponse(f"Песочница для кода питона {fid_id}")


def pageNotFound(request, exception):
    return HttpResponseNotFound("Page not found!!!")


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'blog_theme/addpage.html '

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # try:
#                 # Blog_theme.objects.create(**form.cleaned_data)
#                 form.save()
#                 return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста!!!')
#     else:
#         form = AddPostForm()
#     return render(request, 'blog_theme/addpage.html', {'form': form, 'title': 'Add new post'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def show_post(request, post_slug):
#     post = get_object_or_404(Blog_theme, slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post_slug,
#     }
#
#     return render(request, 'blog_theme/post.html', context=context)

class ShowPost(DetailView):
    model = Blog_theme
    template_name = 'blog_theme/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        return context


class Blog_themeCategory(ListView):
    model = Blog_theme
    template_name = 'blog_theme/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        # выбираем только те записи, которым соответствует категория по указанному слагу,
        # через kwargs['cat_slug'] мы можем получить переменную 'cat_slug', которая прилетает к нам
        # через url (path('category/<slug:cat_slug>/',), теперь фильтруем все в таблице Blog_theme
        # по фильтру 'cat_slug', если он совпадает с _slug категории cat_, связанной с этой записью.
        return Blog_theme.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context
# def show_category(request, cat_slug):
#     posts = Blog_theme.objects.filter(cat__slug=cat_slug)
#
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'title': 'Отображение по разделам',
#         'cat_selected': cat_slug,
#     }
#
#     return render(request, 'blog_theme/index.html', context=context)
