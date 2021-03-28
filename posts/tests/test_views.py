from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Group, Post

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username="Leon")

        cls.creator_user = Client()
        cls.creator_user.force_login(cls.user)

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
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            "index.html": reverse("index"),
            "group.html": reverse("group", kwargs={"slug": "test-slag"}),
            "new.html": reverse("new"),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_context_index_page(self):
        """ Тест контекст index.html"""
        response = self.creator_user.get(reverse("index"))
        self.assertEqual(
            response.context.get("page")[0].text, self.post.text)
        self.assertEqual(
            response.context.get("page")[0].author.username,
            self.post.author.username)
        self.assertEqual(
            response.context.get("page")[0].group.title, self.post.group.title)

    def test_group_pages_show_correct_context(self):
        response = self.creator_user.get(
            reverse("group", args=[self.group.slug])
        )
        self.assertEqual(
            response.context.get("group").title, self.group.title)

    def test_content_new(self):
        """Тесе контент new.html"""
        response = self.creator_user.get(reverse("new"))
        self.assertIsInstance(
            response.context.get("form").fields.get("text"),
            forms.fields.CharField)
        self.assertIsInstance(
            response.context.get("form").fields.get("group"),
            forms.fields.ChoiceField)

    def test_create_content_index(self):
        """Тест создания поста index.html"""
        new_post = Post.objects.create(
            text="тестовый текст",
            author=self.user,
            group=self.group
        )
        response = self.creator_user.get(reverse("index"))
        self.assertContains(response, new_post)

    def test_create_content_group(self):
        """Тест создания поста group.html"""
        new_post = Post.objects.create(
            text="тестовый текст",
            author=self.user,
            group=self.group
        )
        response = self.creator_user.get(
            reverse("group", args=["test-slag"]))
        self.assertContains(response, new_post)


class PaginatorViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username="Alex")
        Group.objects.create(
            title="Название группы",
            slug="test-slug",
            description="тестовый текст"
        )
        cls.group = Group.objects.first()
        for i in range(13):
            Post.objects.create(
                text="Тестовый текст",
                author=user,
                group=cls.group
            )

    def setUp(self):
        self.guest_client = Client()

    def first_page_contains(self):
        templates_url_names = {
            reverse("index"): 10,
            reverse("group",
                    kwargs={"slug": "test-slug"}): 10}

        for value, expected in templates_url_names.items():
            with self.subTest(value=value):
                responce = self.guest_client.get(value)
                self.assertEqual(responce, expected)
            
