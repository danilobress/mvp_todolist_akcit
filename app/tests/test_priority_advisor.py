import pytest
import pytest_asyncio
import respx
import httpx
from app.services.priority_advisor import PriorityAdvisorClient
from app.schemas.task import TaskPriority


@pytest_asyncio.fixture
async def async_http_client():
    async with httpx.AsyncClient() as client:
        yield client


@pytest.fixture
def priority_advisor(async_http_client):
    # Inicializa o PriorityAdvisorClient com um cliente HTTP real (mas que será mockado)
    return PriorityAdvisorClient(async_http_client)


@pytest.mark.asyncio
@respx.mock
async def test_suggest_priority_success_returns_valid_priority(priority_advisor):
    # Arrange
    priority_advisor.api_key = "dummy_key"
    title = "Corrigir bug crítico"
    description = "Usuários não conseguem finalizar compra"

    mock_url = priority_advisor.api_url
    respx.post(mock_url).mock(
        return_value=httpx.Response(
            200, json={"choices": [{"message": {"content": "Alta"}}]}
        )
    )

    # Act
    result = await priority_advisor.suggest_priority(title, description)

    # Assert
    assert result == TaskPriority.ALTA


@pytest.mark.asyncio
async def test_suggest_priority_fallback_without_api_key(priority_advisor):
    # Arrange
    # Removendo a API Key para forçar o sistema a não fazer a chamada externa
    priority_advisor.api_key = ""
    title = "Resolver falha no servidor urgente"
    description = "O servidor está fora do ar."

    # Act
    result = await priority_advisor.suggest_priority(title, description)

    # Assert
    # Baseado no contrato estrito (TDD), o fallback deve retornar "Média"
    assert result == TaskPriority.MEDIA


@pytest.mark.asyncio
@respx.mock
async def test_suggest_priority_timeout_triggers_fallback(priority_advisor):
    # Arrange
    priority_advisor.api_key = "dummy_key"
    title = "Ação urgente requerida no banco"
    description = "Tabelas com lentidão."

    mock_url = priority_advisor.api_url

    # Simulando um Timeout na chamada de rede externa
    respx.post(mock_url).mock(
        side_effect=httpx.TimeoutException("Connection timed out")
    )

    # Act
    result = await priority_advisor.suggest_priority(title, description)

    # Assert
    # O sistema não deve levantar exceção, mas sim capturar o erro e aplicar o fallback "Média"
    assert result == TaskPriority.MEDIA
