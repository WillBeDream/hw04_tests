from django.test import TestCase
from ..models import Group, Post

from django.contrib.auth import get_user_model


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = get_user_model().objects.create_user(username="Leon")

        cls.Group = Group.objects.create(
            title="Какое то название",
            slug="test-site",
            description="какое то описание")

        cls.Post = Post.objects.create(
            text="Красивое описание",
            group=cls.Group,
            author=cls.user)

    def test_verbose_name_test(self):
        group = PostModelTest.Group
        field_verboses = {
            "title": "название",
            "slug": "адрес сообщества",
            "description": "ваше описание"}

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def text_help_test(self):
        post = PostModelTest.Post
        field_help_texts = {
            "text": "напишите текст",
            "group": "название сообщества"}
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_text_label(self):
        post = PostModelTest.Post
        returned_object = post.text[:15]
        self.assertEquals(returned_object, str(post))

    def test_group_label(self):
        group = PostModelTest.Group
        returned_object = group.title
        self.assertEquals(returned_object, str(group))
