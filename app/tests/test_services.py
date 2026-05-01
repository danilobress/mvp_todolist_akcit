import pytest
import logging
from unittest.mock import AsyncMock, MagicMock
from contextlib import asynccontextmanager
from fastapi import BackgroundTasks

from app.services.task_services import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskPriority


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def mock_ai_client():
    return AsyncMock()


@pytest.fixture
def mock_bg_repo():
    return AsyncMock()


@pytest.fixture
def mock_bg_repo_factory(mock_bg_repo):
    @asynccontextmanager
    async def _factory():
        yield mock_bg_repo

    return MagicMock(side_effect=_factory)


@pytest.fixture
def task_service(mock_repo, mock_ai_client, mock_bg_repo_factory):
    return TaskService(
        repo=mock_repo, ai_client=mock_ai_client, bg_repo_factory=mock_bg_repo_factory
    )


@pytest.mark.asyncio
async def test_create_task_assigns_default_priority_and_adds_background_task(
    task_service, mock_repo
):
    # Arrange
    task_data = TaskCreate(title="Test Task", description="Test Description")
    mock_bg_tasks = MagicMock(spec=BackgroundTasks)

    expected_response = TaskResponse(
        id=1,
        title="Test Task",
        description="Test Description",
        is_completed=False,
        priority=TaskPriority.MEDIA,
    )
    mock_repo.create_task.return_value = expected_response

    # Act
    result = await task_service.create_task(task_data, background_tasks=mock_bg_tasks)

    # Assert
    mock_repo.create_task.assert_awaited_once_with(
        task_data, initial_priority=TaskPriority.MEDIA.value
    )
    mock_bg_tasks.add_task.assert_called_once()
    assert result == expected_response


@pytest.mark.asyncio
async def test_get_task_returns_task_when_found(task_service, mock_repo):
    # Arrange
    task_id = 1
    expected_response = TaskResponse(
        id=task_id,
        title="Test Task",
        description="Test",
        is_completed=False,
        priority=TaskPriority.ALTA,
    )
    mock_repo.get_task.return_value = expected_response

    # Act
    result = await task_service.get_task(task_id)

    # Assert
    mock_repo.get_task.assert_awaited_once_with(task_id)
    assert result == expected_response


@pytest.mark.asyncio
async def test_get_task_returns_none_when_id_not_found(task_service, mock_repo):
    # Arrange
    task_id = 999
    mock_repo.get_task.return_value = None

    # Act
    result = await task_service.get_task(task_id)

    # Assert
    assert result is None
    mock_repo.get_task.assert_awaited_once_with(task_id)


@pytest.mark.asyncio
async def test_get_tasks_returns_list_of_tasks(task_service, mock_repo):
    # Arrange
    expected_list = [
        TaskResponse(
            id=1,
            title="Task 1",
            description=None,
            is_completed=False,
            priority=TaskPriority.MEDIA,
        ),
        TaskResponse(
            id=2,
            title="Task 2",
            description=None,
            is_completed=True,
            priority=TaskPriority.ALTA,
        ),
    ]
    mock_repo.get_tasks.return_value = expected_list

    # Act
    result = await task_service.get_tasks(is_completed=None, priority=None)

    # Assert
    mock_repo.get_tasks.assert_awaited_once_with(is_completed=None, priority=None)
    assert result == expected_list


@pytest.mark.asyncio
async def test_update_task_returns_updated_task_when_found(task_service, mock_repo):
    # Arrange
    task_id = 1
    update_data = TaskUpdate(title="Updated Title")
    expected_response = TaskResponse(
        id=task_id,
        title="Updated Title",
        description="Test",
        is_completed=False,
        priority=TaskPriority.MEDIA,
    )
    mock_repo.update_task.return_value = expected_response

    # Act
    result = await task_service.update_task(task_id, update_data)

    # Assert
    mock_repo.update_task.assert_awaited_once_with(task_id, {"title": "Updated Title"})
    assert result == expected_response


@pytest.mark.asyncio
async def test_update_task_empty_payload_returns_current_state(task_service, mock_repo):
    # Arrange
    task_id = 1
    update_data = TaskUpdate()  # Payload vazio, sem campos definidos
    expected_response = TaskResponse(
        id=task_id,
        title="Old Title",
        description=None,
        is_completed=False,
        priority=TaskPriority.MEDIA,
    )
    mock_repo.get_task.return_value = expected_response

    # Act
    result = await task_service.update_task(task_id, update_data)

    # Assert
    mock_repo.get_task.assert_awaited_once_with(task_id)
    mock_repo.update_task.assert_not_called()
    assert result == expected_response


@pytest.mark.asyncio
async def test_update_task_returns_none_when_id_not_found(task_service, mock_repo):
    # Arrange
    task_id = 999
    update_data = TaskUpdate(title="Updated Title")
    mock_repo.update_task.return_value = None

    # Act
    result = await task_service.update_task(task_id, update_data)

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_delete_task_returns_true_when_successful(task_service, mock_repo):
    # Arrange
    task_id = 1
    mock_repo.delete_task.return_value = True

    # Act
    result = await task_service.delete_task(task_id)

    # Assert
    mock_repo.delete_task.assert_awaited_once_with(task_id)
    assert result is True


@pytest.mark.asyncio
async def test_delete_task_returns_false_when_id_not_found(task_service, mock_repo):
    # Arrange
    task_id = 999
    mock_repo.delete_task.return_value = False

    # Act
    result = await task_service.delete_task(task_id)

    # Assert
    assert result is False


@pytest.mark.asyncio
async def test_fetch_and_update_priority_bg_updates_db_when_priority_changes(
    task_service, mock_ai_client, mock_bg_repo, mock_bg_repo_factory
):
    # Arrange
    mock_ai_client.suggest_priority.return_value = TaskPriority.ALTA

    # Act
    await task_service._fetch_and_update_priority_bg(1, "Title", "Desc")

    # Assert
    mock_ai_client.suggest_priority.assert_awaited_once_with("Title", "Desc")
    mock_bg_repo_factory.assert_called_once()
    mock_bg_repo.update_task_priority.assert_awaited_once_with(
        1, TaskPriority.ALTA.value
    )


@pytest.mark.asyncio
async def test_fetch_and_update_priority_bg_skips_update_when_priority_is_media(
    task_service, mock_ai_client, mock_bg_repo, mock_bg_repo_factory
):
    # Arrange
    mock_ai_client.suggest_priority.return_value = TaskPriority.MEDIA

    # Act
    await task_service._fetch_and_update_priority_bg(1, "Title", "Desc")

    # Assert
    mock_bg_repo_factory.assert_not_called()
    mock_bg_repo.update_task_priority.assert_not_called()


@pytest.mark.asyncio
async def test_fetch_and_update_priority_bg_handles_exception(
    task_service, mock_ai_client, caplog
):
    # Arrange
    mock_ai_client.suggest_priority.side_effect = Exception("Erro catastrófico forçado")

    # Act
    with caplog.at_level(logging.ERROR):
        await task_service._fetch_and_update_priority_bg(1, "Title", "Desc")

    # Assert
    assert (
        "Erro na background task de prioridade da Tarefa 1: Erro catastrófico forçado"
        in caplog.text
    )
