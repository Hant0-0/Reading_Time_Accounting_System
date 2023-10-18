# time_reading_system/tests/test_views.py
import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from time_reading_system.models import Book, SessionReading, UserProfile
from django.test import TestCase
from time_reading_system.serializers import BookSerializer


@pytest.mark.django_db
def test_books_api_get():
    # Створення тестової книги для перевірки
    Book.objects.create(
        title="Test Book",
        author="Test Author",
        year_of_published=2022,
        short_description="Short Description",
        full_description="Full Description"
    )

    client = APIClient()
    url = reverse('books-list')

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


