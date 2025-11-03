import pytest
import os
from fastapi.testclient import TestClient
from app.main import app

# Configurar ambiente para usar mocks
os.environ["USE_MOCK"] = "true"


@pytest.fixture
def client():
    """Fixture para criar cliente de teste"""
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Fixture com dados de exemplo para usuário"""
    return {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30}


@pytest.fixture
def sample_users_data():
    """Fixture com dados de exemplo para múltiplos usuários"""
    return [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 25},
    ]


@pytest.fixture
def new_user_data():
    """Fixture com dados para criar novo usuário"""
    return {"name": "New User", "email": "new@example.com", "age": 28}
