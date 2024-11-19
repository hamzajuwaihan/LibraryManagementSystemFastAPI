from typing import Iterable
import pytest
from fastapi.testclient import TestClient

from replace_domain.app import app


@pytest.fixture(scope='session')
def client() -> Iterable[TestClient]:
    client = TestClient(app)
    yield client
