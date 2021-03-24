from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Group, Post


User = get_user_model()


class StaticURLTests(TestCase):
    def test_homepage(self):

        guest_client = Client()

        response = guest_client.get('/')

        self.assertEqual(response.status_code, 200)


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username="Leon")

        cls.Group = Group.objects.create(
            title="Какое то название",
            slug="test-slag",
            description="какое то описание")

        cls.Post = Post.objects.create(
            text="Красивое описание",
            group=cls.Group,
            author=cls.user)

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='AndreyG')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            "index.html": "/",
            "group.html": "/group/test-slag/",
            "new.html": "/new/"}

        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail_url_exists_at_desired_location_authorized(self):
        """Страница /group/test-slug/ доступна авторизованному
        пользователю."""
        response = self.authorized_client.get('/group/test-slag/')
        self.assertEqual(response.status_code, 200)

    def test_task_added_url_exists_at_desired_location(self):
        """Страница /new/ доступна любому пользователю."""
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 200)
