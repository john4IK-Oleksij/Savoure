from datetime import date, timedelta
from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from blog.models import BlogPost
from menu.models import Category, Dish
from reservations.models import ContactMessage, Reservation


class SavoureIntegrationTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.category = Category.objects.create(name="Appetizer", slug="appetizer", order=1)
        self.dish = Dish.objects.create(
            category=self.category,
            title="Tartare de Boeuf",
            slug="tartare-de-boeuf",
            price=Decimal("18.00"),
            description="Hand-cut prime beef tartare with capers and quail egg.",
            is_available=True,
            is_chef_special=True,
        )
        self.blog_post = BlogPost.objects.create(
            title="Autumn Truffle Season",
            slug="autumn-truffle-season",
            description="Discover our rare black truffle culinary arrivals.",
            content="Full story about black truffles and wine pairings.",
            published_at=date.today(),
            is_published=True,
        )

    def test_home_page_status_and_context(self) -> None:
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tartare de Boeuf")
        self.assertContains(response, "Autumn Truffle Season")

    def test_menu_page_and_api(self) -> None:
        response = self.client.get(reverse("menu:dish_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tartare de Boeuf")

        api_res = self.client.get(reverse("menu:api_dishes"))
        self.assertEqual(api_res.status_code, 200)
        json_data = api_res.json()
        self.assertEqual(len(json_data["dishes"]), 1)
        self.assertEqual(json_data["dishes"][0]["title"], "Tartare de Boeuf")

    def test_reservation_get_and_post_valid(self) -> None:
        response = self.client.get(reverse("reservations:reserve"))
        self.assertEqual(response.status_code, 200)

        future_date = date.today() + timedelta(days=3)
        post_data = {
            "name": "Jean Dupont",
            "email": "jean.dupont@example.com",
            "phone": "+33 6 12 34 56 78",
            "date": future_date.strftime("%Y-%m-%d"),
            "time": "19:30",
            "guests": "4",
            "special_request": "Window table please",
        }
        post_res = self.client.post(reverse("reservations:reserve"), data=post_data)
        self.assertEqual(post_res.status_code, 302)
        self.assertTrue(Reservation.objects.filter(email="jean.dupont@example.com").exists())

    def test_reservation_past_date_fails(self) -> None:
        past_date = date.today() - timedelta(days=2)
        post_data = {
            "name": "Past Visitor",
            "email": "past@example.com",
            "phone": "+33 6 00 00 00 00",
            "date": past_date.strftime("%Y-%m-%d"),
            "time": "19:00",
            "guests": "2",
        }
        post_res = self.client.post(reverse("reservations:reserve"), data=post_data)
        self.assertEqual(post_res.status_code, 200)
        self.assertFalse(Reservation.objects.filter(email="past@example.com").exists())

    def test_contact_submission(self) -> None:
        post_data = {
            "name": "Marie Curie",
            "email": "marie@curie.fr",
            "phone": "+33 6 99 88 77 66",
            "message": "We would like to book a private dining room for 15 guests.",
        }
        res = self.client.post(reverse("reservations:contact_submit"), data=post_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email="marie@curie.fr").exists())

    def test_blog_list_and_detail(self) -> None:
        list_res = self.client.get(reverse("blog:blog_list"))
        self.assertEqual(list_res.status_code, 200)
        self.assertContains(list_res, "Autumn Truffle Season")

        detail_res = self.client.get(reverse("blog:detail", kwargs={"slug": self.blog_post.slug}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, "Autumn Truffle Season")

    def test_static_pages(self) -> None:
        pages = ["core:about", "core:findus", "core:privacy", "core:terms"]
        for page_name in pages:
            with self.subTest(page=page_name):
                res = self.client.get(reverse(page_name))
                self.assertEqual(res.status_code, 200)
