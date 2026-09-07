import pytest
from app import create_app
from app.database.base import init_db

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client
