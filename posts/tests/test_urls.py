from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post


User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username="Leon")

        cls.group = Group.objects.create(
            title="Какое то название",
            slug="test-slag",
            description="какое то описание")

        cls.post = Post.objects.create(
            text="Красивое описание",
            group=cls.group,
            author=cls.user)

        cls.templates_url_names = {
            reverse("index"): "index.html",
            reverse("new"): "new.html",
            reverse("group",
                    kwargs={"slug": cls.group.slug}): "group.html",
            reverse("profile",
                    kwargs={"username": cls.user.username}): "profile.html",
            reverse("post",
                    kwargs={"username": cls.user.username,
                            "post_id": cls.post.id}): "post.html"}

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='AndreyG')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_other_pages_authorized_user_templates(self):
        for page, template in self.templates_url_names.items():
            response = self.authorized_client.get(page)
            self.assertTemplateUsed(response, template,
                                    f"{page} шаблон {template} не работает")

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail_url_exists_at_desired_location_authorized(self):
        """Страница /group/test-slug/ доступна авторизованному
        пользователю."""
        response = self.authorized_client.get('/group/test-slag/')
        self.assertEqual(response.status_code, 200)

    def test_post_page_exists_at_desired_location_authorized(self):
        """Cтраница /new/ доступна авторизированным пользователям"""
        response = self.authorized_client.get("/new/")
        self.assertEqual(response.status_code, 200)

    def test_post_edit_guest_client_200(self):
        """Проверки для страницы post_edit(post_new.html)"""
        response = self.guest_client.get(
            reverse("post_edit",
                    kwargs={"username": self.user.username,
                            "post_id": 1}), follow=True)
        self.assertEqual(response.status_code, 200,
                         "post_edit пользователь гость не может зайти.")
