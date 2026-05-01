from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import AsyncGenerator
import httpx
from fastapi import FastAPI, status, Depends, BackgroundTasks, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

from app.models.task import Base
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskPriority
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisorClient
from app.services.task_services import TaskService

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração minimalista de banco de dados local
DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Cliente HTTP Singleton para prevenir exaustão de sockets
http_client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação FastAPI.
    Inicia o cliente HTTP compartilhado e cria tabelas no banco de dados.
    No encerramento, fecha as conexões adequadamente.
    """
    global http_client
    http_client = httpx.AsyncClient()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await http_client.aclose()
    await engine.dispose()


app = FastAPI(
    title="API do Gerenciador de Tarefas PriorityAdvisor",
    description="Uma API minimalista para gerenciar tarefas com sugestões de prioridade baseadas em IA.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuração do CORS (obrigatório pelo GEMINI.md)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # Em produção deve ser restrito às origens reais
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependências (Dependency Injection) ---


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Fornece uma sessão assíncrona do SQLAlchemy estrita para cada requisição."""
    async with async_session_maker() as session:
        yield session


def get_priority_advisor_client() -> PriorityAdvisorClient:
    """
    Fornece uma instância do cliente de integração de IA, reaproveitando o Singleton HTTP.

    Raises:
        RuntimeError: Se o cliente HTTP não tiver sido inicializado no lifespan da aplicação.
    """
    if http_client is None:
        raise RuntimeError("HTTP Client is not initialized")
    return PriorityAdvisorClient(http_client)


def get_task_service(
    db: AsyncSession = Depends(get_db),
    ai_client: PriorityAdvisorClient = Depends(get_priority_advisor_client),
) -> TaskService:
    """Injeta o TaskService com suas dependências: repositório, cliente de IA e a fábrica de sessões."""
    repository = TaskRepository(db)

    @asynccontextmanager
    async def bg_repo_factory():
        async with async_session_maker() as session:
            yield TaskRepository(session)

    return TaskService(repository, ai_client, bg_repo_factory)


# --- Endpoints ---


class HealthCheckResponse(BaseModel):
    """Modelo Pydantic para a resposta de verificação de integridade (health check)."""

    status: str = Field(..., description="O status operacional atual da API")
    timestamp: datetime = Field(
        ..., description="O carimbo de data/hora UTC da verificação de integridade"
    )


@app.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Executar uma verificação de integridade",
    tags=["Monitoramento"],
)
def health_check() -> HealthCheckResponse:
    """Retorna o status da API para fins de monitoramento."""
    return HealthCheckResponse(status="ok", timestamp=datetime.now(timezone.utc))


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova tarefa",
    description=(
        "Cria uma nova tarefa no banco de dados. \n\n"
        "**Requisitos:**\n"
        "- **title**: Obrigatório (mínimo 1 caractere).\n"
        "- **description**: Opcional.\n\n"
        "O sistema aciona silenciosamente uma IA em background para sugerir a prioridade ideal."
    ),
    tags=["Tarefas"],
)
async def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Cria uma nova tarefa no banco de dados.
    Aciona silenciosamente uma IA em background para sugerir a prioridade ideal.
    """
    return await service.create_task(task, background_tasks)


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas as tarefas",
    tags=["Tarefas"],
)
async def list_tasks(
    is_completed: bool | None = Query(
        None, description="Filtrar pelo status de conclusão da tarefa"
    ),
    priority: TaskPriority | None = Query(
        None, description="Filtrar por nível de prioridade (ex: Alta, Média, Baixa)"
    ),
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    """
    Recupera a lista de tarefas, permitindo a filtragem via query parameters.
    """
    priority_value = priority.value if priority else None
    return await service.get_tasks(is_completed=is_completed, priority=priority_value)


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar os detalhes de uma tarefa",
    tags=["Tarefas"],
)
async def get_task(
    task_id: int, service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """
    Recupera os detalhes de uma única tarefa baseada no seu identificador.

    Raises:
        HTTPException: 404 caso o task_id fornecido não exista no banco de dados.
    """
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada"
        )
    return task


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar parcialmente uma tarefa",
    tags=["Tarefas"],
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Atualiza os dados de uma tarefa existente (PATCH).
    Permite alterar o título, descrição, prioridade e marcar como concluída/pendente.

    Raises:
        HTTPException: 404 caso o task_id fornecido não exista no banco de dados.
    """
    updated_task = await service.update_task(task_id, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada"
        )
    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar uma tarefa permanentemente",
    tags=["Tarefas"],
)
async def delete_task(
    task_id: int, service: TaskService = Depends(get_task_service)
) -> None:
    """
    Remove uma tarefa definitivamente do banco de dados do sistema.

    Raises:
        HTTPException: 404 caso o task_id fornecido não exista no banco de dados.
    """
    deleted = await service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada"
        )
