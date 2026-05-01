from typing import Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse


class TaskRepository:
    """
    Repositório para a entidade Task.
    Abstrai as operações de banco de dados e retorna sempre DTOs Pydantic.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa o repositório com uma sessão assíncrona do SQLAlchemy.
        A sessão deve ser injetada via Dependency Injection (DI).
        """
        self.session = session

    # --- Helpers Privados (DRY) ---

    async def _get_task_model(self, task_id: int) -> Task | None:
        """Helper interno para buscar a entidade SQLAlchemy evitando repetição de query."""
        stmt = select(Task).where(Task.id == task_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def _to_dto(self, task_model: Task) -> TaskResponse:
        """Helper interno para centralizar o mapeamento ORM -> DTO Pydantic."""
        return TaskResponse.model_validate(task_model)

    # --- Métodos Públicos (Contratos Imutáveis) ---

    async def create_task(
        self, task_data: TaskCreate, initial_priority: str = "Média"
    ) -> TaskResponse:
        """
        Cria uma nova tarefa no banco de dados.
        """
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=initial_priority,
        )
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)

        return self._to_dto(new_task)

    async def get_task(self, task_id: int) -> TaskResponse | None:
        """
        Busca uma tarefa específica pelo seu ID.
        Retorna None caso não seja encontrada.
        """
        task = await self._get_task_model(task_id)
        return self._to_dto(task) if task else None

    async def get_tasks(
        self, is_completed: bool | None = None, priority: str | None = None
    ) -> list[TaskResponse]:
        """
        Retorna uma lista de tarefas, permitindo a filtragem dinâmica opcional
        por status de conclusão e prioridade.
        """
        stmt = select(Task)

        if is_completed is not None:
            stmt = stmt.where(Task.is_completed == is_completed)

        if priority is not None:
            stmt = stmt.where(Task.priority == priority)

        result = await self.session.execute(stmt)
        tasks = result.scalars().all()

        return [self._to_dto(task) for task in tasks]

    async def update_task(
        self, task_id: int, update_data: dict[str, Any]
    ) -> TaskResponse | None:
        """
        Atualiza dinamicamente os campos de uma tarefa (PATCH).
        Retorna a tarefa atualizada ou None se não for encontrada.
        """
        task = await self._get_task_model(task_id)
        if not task:
            return None

        for key, value in update_data.items():
            setattr(task, key, value)

        await self.session.commit()
        await self.session.refresh(task)

        return self._to_dto(task)

    async def update_task_priority(self, task_id: int, priority: str) -> None:
        """
        Atualiza diretamente a prioridade de uma tarefa (acionado geralmente por processos em background).
        """
        stmt = update(Task).where(Task.id == task_id).values(priority=priority)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_task(self, task_id: int) -> bool:
        """
        Remove permanentemente uma tarefa do banco de dados pelo seu ID.
        Retorna True se deletou com sucesso, False se a tarefa não existia.
        """
        stmt = delete(Task).where(Task.id == task_id)
        result = await self.session.execute(stmt)
        await self.session.commit()

        # Utiliza getattr para contornar o alerta do Pylance, pois a classe base Result
        # não mapeia explicitamente a propriedade rowcount do CursorResult.
        return getattr(result, "rowcount", 0) > 0
