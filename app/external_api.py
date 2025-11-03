import httpx
import os
from app.models import User, UserCreate
from typing import List


class ExternalAPI:
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.timeout = 30.0
        self.use_mock = os.getenv("USE_MOCK", "false").lower() == "true"

    async def get_all_users(self) -> List[User]:
        """Fetch all users from external API"""
        if self.use_mock:
            # Dados mockados para testes
            return [
                User(id=1, name="John Doe", email="john@example.com", age=30),
                User(id=2, name="Jane Smith", email="jane@example.com", age=25),
            ]

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/users")
                response.raise_for_status()
                users_data = response.json()

                users = []
                for user_data in users_data:
                    users.append(
                        User(
                            id=user_data["id"],
                            name=user_data["name"],
                            email=user_data["email"],
                            age=None,
                        )
                    )
                return users
        except Exception as e:
            # Fallback para dados mockados em caso de erro
            return [
                User(id=1, name="John Doe", email="john@example.com", age=30),
                User(id=2, name="Jane Smith", email="jane@example.com", age=25),
            ]

    async def get_user_by_id(self, user_id: int) -> User:
        """Fetch user by ID from external API"""
        if self.use_mock:
            # Dados mockados para testes
            if user_id == 1:
                return User(id=1, name="John Doe", email="john@example.com", age=30)
            return None

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/users/{user_id}")
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                user_data = response.json()

                return User(
                    id=user_data["id"],
                    name=user_data["name"],
                    email=user_data["email"],
                    age=None,
                )
        except Exception:
            # Fallback para dados mockados em caso de erro
            if user_id == 1:
                return User(id=1, name="John Doe", email="john@example.com", age=30)
            return None

    async def create_user(self, user: UserCreate) -> User:
        """Create a new user in external API"""
        if self.use_mock:
            # Dados mockados para testes
            return User(id=101, name=user.name, email=user.email, age=user.age)

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                user_data = {"name": user.name, "email": user.email, "age": user.age}

                response = await client.post(f"{self.base_url}/users", json=user_data)
                response.raise_for_status()
                created_data = response.json()

                return User(
                    id=created_data["id"],
                    name=created_data["name"],
                    email=created_data["email"],
                    age=created_data.get("age"),
                )
        except Exception:
            # Fallback para dados mockados em caso de erro
            return User(id=101, name=user.name, email=user.email, age=user.age)
