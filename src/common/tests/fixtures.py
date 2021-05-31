import pytest
from django.test.client import Client as DjangoTestClient
from faker import Faker
from faker.providers import BaseProvider

faker = Faker()


class Provider(BaseProvider):
    pass


faker.add_provider(Provider)


@pytest.fixture(scope='session')
def fake():
    return faker


@pytest.fixture
@pytest.mark.django_db
def api_client_factory(client):
    def create_api_client():
        c_type = 'application/json'

        class ApiClient(DjangoTestClient):

            def get(self, path, data=None, **extra):
                return super().get(path, data, content_type=c_type, **extra)

            def post(self, path, data=None, **extra):
                return super().post(path, data, content_type=c_type, **extra)

            def put(self, path, data=None, **extra):
                return super().put(path, data, content_type=c_type, **extra)

            def patch(self, path, data=None, **extra):
                return super().patch(path, data, content_type=c_type, **extra)

            def delete(self, path, data=None, **extra):
                return super().delete(path, data, content_type=c_type, **extra)

        api_client = ApiClient()
        return api_client

    return create_api_client


class Equal:
    def __eq__(self, other):
        return True
