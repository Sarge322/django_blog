from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import pre_save
from pytils.translit import slugify



class Blog_theme(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликованно')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Раздел')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Темы:'
        verbose_name_plural = 'Темы:'
        ordering = ['time_created', 'title']


@receiver(pre_save, sender=Blog_theme)
def store_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Раздел')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Раздел:'
        verbose_name_plural = 'Разделы:'
        ordering = ['id']
