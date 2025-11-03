from unittest.mock import patch
from app.models import User


class TestUserEndpoints:
    """Testes para os endpoints de usuários"""

    def test_get_all_users_success(self, client, sample_users_data):
        """Teste de sucesso para listar todos os usuários"""
        # Criar objetos User a partir dos dados de fixture
        mock_users = [User(**user_data) for user_data in sample_users_data]

        # Mock da função externa
        with patch("app.main.external_api.get_all_users", return_value=mock_users):
            response = client.get("/users")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "John Doe"
            assert data[1]["email"] == "jane@example.com"

    def test_get_all_users_failure(self, client):
        """Teste de falha para listar todos os usuários"""
        # Mock para simular erro
        with patch(
            "app.main.external_api.get_all_users", side_effect=Exception("API Error")
        ):
            response = client.get("/users")

            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "API Error" in data["detail"]

    def test_get_user_by_id_success(self, client, sample_user_data):
        """Teste de sucesso para buscar usuário por ID"""
        mock_user = User(**sample_user_data)

        with patch("app.main.external_api.get_user_by_id", return_value=mock_user):
            response = client.get("/users/1")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["name"] == "John Doe"
            assert data["email"] == "john@example.com"

    def test_get_user_by_id_not_found(self, client):
        """Teste de falha para buscar usuário por ID (não encontrado)"""
        with patch("app.main.external_api.get_user_by_id", return_value=None):
            response = client.get("/users/999")

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "User not found"

    def test_get_user_by_id_failure(self, client):
        """Teste de falha para buscar usuário por ID (erro interno)"""
        with patch(
            "app.main.external_api.get_user_by_id",
            side_effect=Exception("Internal Error"),
        ):
            response = client.get("/users/1")

            assert response.status_code == 500
            data = response.json()
            assert "detail" in data

    def test_create_user_success(self, client, new_user_data):
        """Teste de sucesso para criar novo usuário"""
        created_user = User(id=101, **new_user_data)

        with patch("app.main.external_api.create_user", return_value=created_user):
            response = client.post("/users", json=new_user_data)

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 101
            assert data["name"] == new_user_data["name"]
            assert data["email"] == new_user_data["email"]
            assert data["age"] == new_user_data["age"]

    def test_create_user_failure(self, client, new_user_data):
        """Teste de falha para criar novo usuário"""
        with patch(
            "app.main.external_api.create_user",
            side_effect=Exception("Creation failed"),
        ):
            response = client.post("/users", json=new_user_data)

            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "Creation failed" in data["detail"]

    def test_root_endpoint(self, client):
        """Teste do endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "User API is running" in data["message"]

    def test_health_check(self, client):
        """Teste do endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
