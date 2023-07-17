from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import MinValueValidator
from django.urls import reverse


class Users(models.Model):
    name = models.CharField(max_length=200)
    profile_data = JSONField(null=True)
    pseudonyms = ArrayField(
        models.CharField(max_length=10, blank=True),
        size=8,
    )

class Author(models.Model):
    name = models.CharField(
        default='NoName',
        max_length=64,
        verbose_name='name of author')


class Article(models.Model):
    object = None
    news = 'NW'
    states = 'PS'

    TYPE = [
        (news, 'Новость'),
        (states, 'Статья')
    ]

    post_tip = models.CharField(max_length=10, choices=TYPE, default=states)
    date_in = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    contents = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(to=Category, through='PostCategory', related_name='PostCategory')
    rating_post = models.IntegerField(default=0, validators=[MinValueValidator(0.0)])

    def likes(self):
        self.rating_post += 1
        self.save()

    def dislikes(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return f"{self.contents[:124]}..."

    def __str__(self):
        return f'{self.header.title()}:{self.contents[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'posts-{self.pk}')
        # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=20, default='местные новости')
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='subscribers')

    def __str__(self):
        return self.name.title()

