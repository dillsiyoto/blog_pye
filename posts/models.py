from django.db import models
from django.utils import timezone

from clients.models import Client


class Posts(models.Model):
    title = models.CharField(
        verbose_name="Название поста",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание",
        max_length=5000,
    )
    date_publication = models.DateTimeField(
        verbose_name="дата публикации",
        default=timezone.now,
    )
    user = models.ForeignKey(
        to=Client,
        verbose_name="автор",
        on_delete=models.SET_DEFAULT,
        default="Unknown author",
        related_name="client_posts",
    )
    likes = models.PositiveBigIntegerField(
        verbose_name="лайки",
        default=0,
    )
    dislikes = models.PositiveBigIntegerField(
        verbose_name="дизлайки",
        default=0,
    )


class Images(models.Model):
    image = models.ImageField(
        verbose_name="изображение",
        upload_to="images/posts/",
    )
    post = models.ForeignKey(
        to=Posts, 
        on_delete=models.CASCADE,
        related_name="post_images",
        verbose_name="статья",
    )
