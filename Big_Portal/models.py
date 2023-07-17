from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models



class User(models.Model):
    pseudonyms = ArrayField(
        models.CharField(max_length=10, blank=True),
        size=8,
    )


class Users(models.Model):
    name = models.CharField(max_length=200)
    profile_data = JSONField(null=True)


class Author(models.Model):
    name = models.CharField(
        default='NoName',
        max_length=64,
        verbose_name='name of author')