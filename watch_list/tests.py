from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from watch_list import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="example",
            email="example@test.com",
            password="test"
        )
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name="Spotify",
            about="Most famous music streaming platform",
            url="https://www.spotify.com/in"
        )

    def test_stream_platform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming platform in india",
            "url": "https://www.netflix.com/"
        }
        response = self.client.post(reverse('streamplatform-list'), data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_platform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="example",
            email="example@test.com",
            password="test"
        )
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name="Spotify",
            about="Most famous music streaming platform",
            url="https://www.spotify.com/in"
        )

        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="Lose Yourself",
            description="One of the best raps around",
            is_active=True
        )

    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "Chandelier",
            "description": "Very popular song from sia",
            "is_active": True
        }

        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_detail(self):
        # Sending an unauthenticated request
        client_unauthenticated = APIClient()
        response = client_unauthenticated.get(reverse("watchlist-detail", args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'Lose Yourself')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="example",
            email="example@test.com",
            password="test"
        )
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name="Spotify",
            about="Most famous music streaming platform",
            url="https://www.spotify.com/in"
        )

        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="Lose Yourself",
            description="One of the best raps around",
            is_active=True
        )

        self.watchlist2 = models.WatchList.objects.create(
            platform=self.stream,
            title="Chandelier",
            description="Great song",
            is_active=True
        )

        self.review = models.Review.objects.create(
            review_user=self.user,
            rating=10,
            description="Pretty great",
            watchlist=self.watchlist2,
            is_active=True
        )

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 10,
            "description": "One of the best raps I have ever heard",
            "watchlist": self.watchlist,
            "is_active": True
        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(models.Review.objects.count(), 2)
        # self.assertEqual(models.Review.objects.get().rating, 10)

        # Adding a review second time using the same user
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauthenticated(self):
        client_unauthenticated = APIClient()
        data = {
            "review_user": self.user,
            "rating": 10,
            "description": "One of the best raps I have ever heard",
            "watchlist": self.watchlist,
            "is_active": True
        }

        response = client_unauthenticated.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 7,
            "description": "One of the best raps I have ever heard - Updated",
            "watchlist": self.watchlist,
            "is_active": False
        }

        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(reverse('review-list', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client_unauthenticated = APIClient()
        response = client_unauthenticated.get(reverse('review-list', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get('/review/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
