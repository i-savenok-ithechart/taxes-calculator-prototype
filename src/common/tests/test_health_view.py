import pytest

from common.http import status

PATH = '/health/'


@pytest.mark.django_db
def test_health_view(api_client_factory):
    response = api_client_factory().get(PATH)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}
