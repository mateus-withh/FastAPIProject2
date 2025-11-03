import pytest
import os
from app.external_api import ExternalAPI
from app.models import UserCreate

# Garantir que use mocks nos testes
os.environ["USE_MOCK"] = "true"

class TestExternalAPI:
    """Testes para a classe ExternalAPI"""
    
    @pytest.mark.asyncio
    async def test_get_all_users_success(self):
        """Teste de sucesso para obter todos os usuários"""
        external_api = ExternalAPI()
        
        users = await external_api.get_all_users()
        
        # Verifica que retorna uma lista
        assert isinstance(users, list)
        # Verifica que tem 2 usuários (do mock)
        assert len(users) == 2
        # Verifica que são objetos User
        assert all(user.__class__.__name__ == "User" for user in users)
        # Verifica os dados específicos do mock
        assert users[0].id == 1
        assert users[0].name == "John Doe"
        assert users[1].email == "jane@example.com"

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self):
        """Teste de sucesso para obter usuário por ID existente"""
        external_api = ExternalAPI()
        
        user = await external_api.get_user_by_id(1)
        
        # Verifica que retorna um usuário
        assert user is not None
        assert user.__class__.__name__ == "User"
        assert user.id == 1
        assert user.name == "John Doe"  # Agora usa o nome do mock

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self):
        """Teste para usuário não encontrado"""
        external_api = ExternalAPI()
        
        user = await external_api.get_user_by_id(999)
        
        # Verifica que retorna None para ID não existente
        assert user is None

    @pytest.mark.asyncio
    async def test_create_user_success(self):
        """Teste de sucesso para criar usuário"""
        external_api = ExternalAPI()
        user_data = UserCreate(
            name="New User",
            email="new@example.com",
            age=25
        )
        
        user = await external_api.create_user(user_data)
        
        # Verifica que retorna um usuário criado
        assert user is not None
        assert user.__class__.__name__ == "User"
        assert user.id == 101  # ID do mock
        assert user.name == "New User"
        assert user.email == "new@example.com"
        assert user.age == 25

    @pytest.mark.asyncio
    async def test_create_user_without_age(self):
        """Teste para criar usuário sem idade"""
        external_api = ExternalAPI()
        user_data = UserCreate(
            name="User Without Age",
            email="noage@example.com"
        )
        
        user = await external_api.create_user(user_data)
        
        # Verifica que cria usuário mesmo sem idade
        assert user is not None
        assert user.name == "User Without Age"
        assert user.email == "noage@example.com"
        assert user.age is None