from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # contribs = models.ManyToManyField('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    visits = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('blog.Tag', blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Tag(models.Model):
    nome = models.CharField(max_length=50)
    # editable excludes from auto form/view generate
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nome

class Reuniao(models.Model):
    assunto = models.CharField(max_length=50)
    data = models.DateTimeField(default=timezone.now, blank=True)
    presenca = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.assunto