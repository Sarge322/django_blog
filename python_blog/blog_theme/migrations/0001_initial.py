# Generated by Django 3.2.16 on 2023-01-13 17:56

from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Раздел')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Раздел:',
                'verbose_name_plural': 'Разделы:',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Blog_theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', mdeditor.fields.MDTextField()),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('time_updated', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликованно')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog_theme.category', verbose_name='Раздел')),
            ],
            options={
                'verbose_name': 'Темы:',
                'verbose_name_plural': 'Темы:',
                'ordering': ['-time_updated', 'title'],
            },
        ),
    ]
