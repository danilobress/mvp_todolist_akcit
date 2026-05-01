from typing import AsyncGenerator
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.models.task import Base, Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskPriority

# Configuração restrita de banco de dados em memória para testes
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Configura e limpa as tabelas do banco em memória para cada teste isoladamente."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fornece uma sessão assíncrona real conectada ao SQLite em memória."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def repository(db_session: AsyncSession) -> TaskRepository:
    """Injeta a sessão de banco no repositório a ser testado."""
    return TaskRepository(db_session)


@pytest.mark.asyncio
async def test_create_task_persists_data_successfully(repository: TaskRepository):
    # Arrange
    task_in = TaskCreate(title="Test Task", description="Testing creation")

    # Act
    task_out = await repository.create_task(
        task_in, initial_priority=TaskPriority.ALTA.value
    )

    # Assert
    assert task_out.id is not None
    assert task_out.title == "Test Task"
    assert task_out.description == "Testing creation"
    assert task_out.is_completed is False
    assert task_out.priority == TaskPriority.ALTA


@pytest.mark.asyncio
async def test_get_task_returns_correct_record(
    repository: TaskRepository, db_session: AsyncSession
):
    # Arrange
    task_model = Task(title="Search Target", priority=TaskPriority.MEDIA.value)
    db_session.add(task_model)
    await db_session.commit()
    await db_session.refresh(task_model)

    # Act
    task_out = await repository.get_task(task_model.id)

    # Assert
    assert task_out is not None
    assert task_out.id == task_model.id
    assert task_out.title == "Search Target"


@pytest.mark.asyncio
async def test_get_task_returns_none_when_id_not_found(repository: TaskRepository):
    # Act
    task_out = await repository.get_task(9999)

    # Assert
    assert task_out is None


@pytest.mark.asyncio
async def test_get_tasks_without_filters_returns_all_records(
    repository: TaskRepository, db_session: AsyncSession
):
    # Arrange
    db_session.add_all(
        [
            Task(title="Task 1", priority=TaskPriority.MEDIA.value),
            Task(title="Task 2", priority=TaskPriority.ALTA.value),
        ]
    )
    await db_session.commit()

    # Act
    tasks = await repository.get_tasks()

    # Assert
    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_get_tasks_filters_by_is_completed_successfully(
    repository: TaskRepository, db_session: AsyncSession
):
    # Arrange
    db_session.add_all(
        [
            Task(title="Pending", is_completed=False),
            Task(title="Done 1", is_completed=True),
            Task(title="Done 2", is_completed=True),
        ]
    )
    await db_session.commit()

    # Act
    completed_tasks = await repository.get_tasks(is_completed=True)
    pending_tasks = await repository.get_tasks(is_completed=False)

    # Assert
    assert len(completed_tasks) == 2
    assert len(pending_tasks) == 1
    assert all(t.is_completed is True for t in completed_tasks)


@pytest.mark.asyncio
async def test_get_tasks_filters_by_priority_successfully(
    repository: TaskRepository, db_session: AsyncSession
):
    # Arrange
    db_session.add_all(
        [
            Task(title="P1", priority=TaskPriority.ALTA.value),
            Task(title="P2", priority=TaskPriority.BAIXA.value),
            Task(title="P3", priority=TaskPriority.ALTA.value),
        ]
    )
    await db_session.commit()

    # Act
    high_priority_tasks = await repository.get_tasks(priority=TaskPriority.ALTA.value)

    # Assert
    assert len(high_priority_tasks) == 2
    assert all(t.priority == TaskPriority.ALTA for t in high_priority_tasks)


@pytest.mark.asyncio
async def test_get_tasks_filters_combined_is_completed_and_priority(
    repository: TaskRepository, db_session: AsyncSession
):
    # Arrange
    db_session.add_all(
        [
            Task(title="Target", is_completed=True, priority=TaskPriority.BAIXA.value),
            Task(
                title="Noise 1", is_completed=False, priority=TaskPriority.BAIXA.value
            ),
            Task(title="Noise 2", is_completed=True, priority=TaskPriority.ALTA.value),
        ]
    )
    await db_session.commit()

    # Act
    tasks = await repository.get_tasks(
        is_completed=True, priority=TaskPriority.BAIXA.value
    )

    # Assert
    assert len(tasks) == 1
    assert tasks[0].title == "Target"


@pytest.mark.asyncio
async def test_update_task_modifies_data_successfully(
    repository: TaskRepository, db_session: AsyncSession
):
    # Arrange
    task_model = Task(title="Old Title", is_completed=False)
    db_session.add(task_model)
    await db_session.commit()
    await db_session.refresh(task_model)

    update_data = {"title": "New Title", "is_completed": True}

    # Act
    task_out = await repository.update_task(task_model.id, update_data)

    # Assert
    assert task_out is not None
    assert task_out.title == "New Title"
    assert task_out.is_completed is True

    # Validate persistence directly in DB
    result = await db_session.get(Task, task_model.id)
    assert result is not None
    assert result.title == "New Title"


@pytest.mark.asyncio
async def test_update_task_priority_modifies_priority_directly(
    repository: TaskRepository, db_session: AsyncSession
):
    # Arrange
    task_model = Task(title="Test", priority=TaskPriority.BAIXA.value)
    db_session.add(task_model)
    await db_session.commit()
    await db_session.refresh(task_model)

    # Act
    task_id = task_model.id
    await repository.update_task_priority(task_id, TaskPriority.ALTA.value)

    # Assert
    # Clears session to force a fresh DB read
    db_session.expunge_all()
    result = await db_session.get(Task, task_id)
    assert result is not None
    assert result.priority == TaskPriority.ALTA.value


@pytest.mark.asyncio
async def test_delete_task_removes_record_from_db(
    repository: TaskRepository, db_session: AsyncSession
):
    # Arrange
    task_model = Task(title="To be deleted")
    db_session.add(task_model)
    await db_session.commit()
    await db_session.refresh(task_model)

    # Act
    success = await repository.delete_task(task_model.id)

    # Assert
    assert success is True
    result = await db_session.get(Task, task_model.id)
    assert result is None


@pytest.mark.asyncio
async def test_delete_task_returns_false_when_id_not_found(repository: TaskRepository):
    # Act
    success = await repository.delete_task(9999)

    # Assert
    assert success is False
