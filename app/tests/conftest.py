import asyncio
import pytest
import httpx
import respx
from contextlib import asynccontextmanager
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.main import app, get_task_service
from app.models.task import Base
from app.repositories.task_repository import TaskRepository
from app.services.task_services import TaskService
from app.services.priority_advisor import PriorityAdvisorClient
from app.config import settings

# Configuração do banco em memória isolado
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


@pytest.fixture(autouse=True)
def setup_db():
    """Garante que o esquema do banco é recriado de forma limpa a cada teste."""

    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def teardown_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(init_db())
    yield
    asyncio.run(teardown_db())


@pytest.fixture
def mock_ai_api():
    """Intercepta as requisições feitas pela IA via httpx usando respx."""
    with respx.mock(assert_all_called=False) as respx_mock:
        respx_mock.post(settings.llm_api_url).mock(
            return_value=httpx.Response(
                200, json={"choices": [{"message": {"content": "Alta"}}]}
            )
        )
        yield respx_mock


@pytest.fixture
def client(mock_ai_api):
    """
    Substitui a injeção de dependência do TaskService por completo para injetar
    o banco de dados transiente e isolar as chamadas http em background.
    """

    async def override_get_task_service():
        async with TestingSessionLocal() as session:
            repository = TaskRepository(session)
            async with httpx.AsyncClient() as http_client:
                ai_client = PriorityAdvisorClient(http_client)

                @asynccontextmanager
                async def bg_repo_factory():
                    async with TestingSessionLocal() as bg_session:
                        yield TaskRepository(bg_session)

                yield TaskService(repository, ai_client, bg_repo_factory)

    app.dependency_overrides[get_task_service] = override_get_task_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
