from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="название",
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="адрес сообщества")
    description = models.TextField(
        verbose_name="ваше описание"
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name="текст",
        help_text="напишите текст"
    )
    pub_date = models.DateTimeField(
        "date published",
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="автор поста",
        help_text="автор")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="posts",
        verbose_name="сообщества",
        help_text="название сообщества")

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:15]
