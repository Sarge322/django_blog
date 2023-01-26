from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
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
from .utils import DataMixin


class BlogHome(DataMixin, ListView):

    # атрибут model ссылается на модель Blog_theme, создается список всех записей модели Blog_theme
    model = Blog_theme
    # прописываем путь нашей страницы
    template_name = 'blog_theme/index.html'
    # передаем список в виде переменной, указаной в шаблоне index.html(posts), object_list - дефолтная переменная
    context_object_name = 'posts'

    # создаем функцию для динамического и стат. контекста
    def get_context_data(self, *, object_list=None, **kwargs):

        # обращаемся к базовому классу ListView и берем существующий контекст, чтобы не создать новый пустой и не затереть все
        context = super().get_context_data(**kwargs)
        #через миксин DataMixin получаеи второй словарь с title='Главная страница',
        #теперь нужно их обьединить и отдать
        c_def = self.get_user_context(title='Главная страница')

        # # меняем атрибут контекста title, отображение имени вкладки
        # context['title'] = 'Главная страница'
        # # передаем дефолтный указатель выбранной категории
        # context['cat_selected'] = 0
        context.update(c_def)
        return context

    # фильтруем только опубликованные статьи (с галкой is_published)
    def get_queryset(self):
        return Blog_theme.objects.filter(is_published=True).select_related('cat')


def about(request):
    contact_list = Blog_theme.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog_theme/about.html', {'page_obj': page_obj, 'title': 'About'})


def python_fiddle(request, fid_id):
    return HttpResponse(f"Песочница для кода питона {fid_id}")


def pageNotFound(request, exception):
    return HttpResponseNotFound("Page not found!!!")


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


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    #связываем класс представления с классом формы из forms.py
    form_class = AddPostForm
    template_name = 'blog_theme/addpage.html '
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        context.update(c_def)
        return context


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'blog_theme/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        context.update(c_def)
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')



# def login(request):
#     return HttpResponse("Авторизация")


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

class ShowPost(DataMixin, DetailView):
    model = Blog_theme
    template_name = 'blog_theme/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context.update(c_def)
        return context


class Blog_themeCategory(DataMixin, ListView):
    paginate_by = 3
    model = Blog_theme
    template_name = 'blog_theme/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        # выбираем только те записи, которым соответствует категория по указанному слагу,
        # через kwargs['cat_slug'] мы можем получить переменную 'cat_slug', которая прилетает к нам
        # через url (path('category/<slug:cat_slug>/',), теперь фильтруем все в таблице Blog_theme
        # по фильтру 'cat_slug', если он совпадает с _slug категории cat_, связанной с этой записью,
        # ну и статья должна быть опубликована.
        return Blog_theme.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        # # присваиваем названию имя категории первого поста в коллекции полученных записей.
        # context['title'] = str(context['posts'][0].cat)
        # # аналогично, из коллекции вытаскиваем id категории первого поста (возможно единственного)
        # context['cat_selected'] = context['posts'][0].cat_id
        # Формирование через миксин DataMixin
        c_def = self.get_user_context(title='Категория' + str(context['posts'][0].cat),
                                        cat_selected=self.kwargs['cat_slug'])
        context.update(c_def)
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

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'blog_theme/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        context.update(c_def)
        return context
    # django func, called if registration was succesful
    def form_valid(self, form):
        user = form.save()
        # login is standart django func, need import, autolotin with
        # previously saved user=form.save() fields values
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'blog_theme/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        context.update(c_def)
        return context

    # def get_success_url(self):
    #     return reverse_lazy('home')

def logout_user(request):
    # logout there is standart django func for logout user, need import
    logout(request)
    return redirect('login')