
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
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_create_post_end_redirect(self): 
        """Тест соханения данных и redirect для new_post""" 
        from_data = { 
            "group": self.group.id, 
            "text": "Тестовый текст", 
        } 
        number_posts = Post.objects.count() 
        response = self.authorized_user.post( 
            reverse("new"), 
            data=from_data, 
            follow=True) 
        self.assertEqual( 
            response.status_code, 

            200, 
            "Страница new.html не отвечает") 
        self.assertEqual( 
            Post.objects.count(), 
            number_posts + 1, 
            "Количество постов меньше 1") 
        self.assertRedirects(response, reverse("index")) 
 
    def test_post_edit_create_post_end_redirect(self): 
        """Тест соханения данных и redirect для post_edit""" 
        from_data = { 
            "group": self.group.id, 
            "text": "Тестовый текст", 
        } 
 
        response = self.authorized_user.post( 
            reverse("post_edit", args=[self.post.author, self.post.id]), 
            data=from_data, follow=True) 
 
        self.assertEqual( 
            response.status_code, 200, 
            "Страница post_new.html не отвечает") 
 
        self.assertEqual( 

            Post.objects.first().text, 
            from_data["text"], 
            "Пост не меняется.") 

    def test_guest_client_cant_edit_posts(self):
        """ неавторизированный пользователь"""
        posts_count = Post.objects.count()
        form_data = {
            "text": "Отредактированный пост", 
            "group": self.group.id,} 
        kwargs = {"username": "Leon", "post_id": self.post.id} 
        response = self.guest_client.post( 
            reverse("post_edit", kwargs=kwargs), 
            data=form_data, 
            follow=True 
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response, reverse("post", kwargs=kwargs))

    def test_guest_client_create_post(self):
        """Не авторизированый пользователь не может создавать новый пост."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'text',
            'group': TaskURLTests.group.id,
        }

        response = self.guest_client.post(
            reverse('new'),
            data=form_data,
            follow=False
        )
        self.assertEqual(response.status_code,302)
        self.assertEqual(Post.objects.count(), post_count)
        self.assertFalse(
            Post.objects.filter(
                text='text',
                group=TaskURLTests.group.id
            ).exists()
        )