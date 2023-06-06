import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestIndexViews:
    client = Client()

    def test_index_rendering(self):
        url = reverse('website:index')
        response = self.client.get(url)
        assert response.status_code == 200
        assert "vini-codex" in response.content.decode("utf-8")


