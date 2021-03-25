
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Group, Post


User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username="Leon")
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user)

        cls.group = Group.objects.create(
            title="Какое то название",
            slug="test-slag",
            description="какое то описание")

        cls.post = Post.objects.create(
            text="Красивое описание",
            group=cls.group,
            author=cls.user)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username="test-name")
        self.authorized_client = Client()
        self.second_authorized_client = Client()
        self.authorized_client.force_login(self.user)
       

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            "text": "Тестовый текст поста",
            "group": self.group.id,
            "author": self.user
        }
        response = self.authorized_client.post(
            reverse("new"),
            data=form_data,
            follow=True,
        )
        new_post = Post.objects.get(text="Тестовый текст поста")
        self.assertEqual(new_post.author, self.user)
        self.assertEqual(new_post.group, self.group)
        self.assertEqual(Post.objects.count(), posts_count + 1)
    
    def test_guest_client_cant_edit_posts(self):
        form_data = {
        "text": "Отредактированный пост",
        "group": self.group.id
        }
        kwargs = {"username": "test-name", "post_id": self.post.id}
        response = self.guest_client.post(
            reverse("post_edit", kwargs=kwargs),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse("post", kwargs=kwargs))