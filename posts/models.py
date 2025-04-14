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

    class Meta:
        ordering = ("id",)
        verbose_name = "статья"
        verbose_name_plural = "статьи"

    def __str__(self):
        return f"{self.title} | {self.date_publication}"


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

    class Meta:
        ordering = ("id",)
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self):
        return f"{self.pk} | {self.image}"


class Categories(models.Model):
    title = models.CharField(
        verbose_name="категория",
        unique=True,
        max_length=50
    )
    post = models.ManyToManyField(
        to=Posts, 
        related_name="posts_categories",
        verbose_name="статья",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return f"{self.pk} | {self.title}"
