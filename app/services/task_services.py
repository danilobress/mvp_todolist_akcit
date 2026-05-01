import logging
from fastapi import BackgroundTasks
from typing import Callable, AsyncContextManager

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskPriority
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisorClient

logger = logging.getLogger(__name__)


class TaskService:
    """
    Camada de Lógica de Negócios (Service) para a entidade Task.
    Orquestra as operações entre o Repositório (banco de dados) e o PriorityAdvisor (IA).
    Retorna estritamente Pydantic DTOs e não lida com requisições HTTP do Controller.
    """

    def __init__(
        self,
        repo: TaskRepository,
        ai_client: PriorityAdvisorClient,
        bg_repo_factory: Callable[[], AsyncContextManager[TaskRepository]],
    ):
        """
        Recebe o Repositório e o Cliente IA via Injeção de Dependência (DI).

        Args:
            repo (TaskRepository): Instância do repositório para persistência.
            ai_client (PriorityAdvisorClient): Cliente para sugerir prioridades usando IA.
            bg_repo_factory (Callable[[], AsyncContextManager[TaskRepository]]): Fábrica assíncrona para instanciar repositórios em background.
        """
        self.repo = repo
        self.ai_client = ai_client
        self.bg_repo_factory = bg_repo_factory

    async def create_task(
        self, task_data: TaskCreate, background_tasks: BackgroundTasks
    ) -> TaskResponse:
        """
        Cria uma nova tarefa aplicando a prioridade padrão ('Média').
        Delega para uma background task a responsabilidade de consultar a IA
        e atualizar a prioridade no banco de forma não bloqueante.

        Args:
            task_data (TaskCreate): DTO com os dados de entrada para criação.
            background_tasks (BackgroundTasks): Gerenciador de tarefas em background do FastAPI.

        Returns:
            TaskResponse: DTO da tarefa recém-criada.
        """
        # 1. Persiste a tarefa de forma rápida com a prioridade padrão
        new_task = await self.repo.create_task(
            task_data, initial_priority=TaskPriority.MEDIA.value
        )

        # 2. Adiciona a rotina de IA em background para não travar a resposta da API
        background_tasks.add_task(
            self._fetch_and_update_priority_bg,
            task_id=new_task.id,
            title=new_task.title,
            description=new_task.description,
        )

        return new_task

    async def _fetch_and_update_priority_bg(
        self, task_id: int, title: str, description: str | None
    ) -> None:
        """
        Método interno executado em background (BackgroundTasks).
        Consulta o PriorityAdvisor e atualiza o banco se a prioridade sugerida for diferente.

        Args:
            task_id (int): ID da tarefa a ser atualizada.
            title (str): Título da tarefa enviado para a IA.
            description (str | None): Descrição da tarefa enviada para a IA.
        """
        try:
            suggested_priority = await self.ai_client.suggest_priority(
                title, description
            )

            if suggested_priority != TaskPriority.MEDIA:
                await self._persist_background_priority(
                    task_id, suggested_priority.value
                )

        except Exception as e:
            # Fallback silencioso extra na orquestração para garantir segurança total
            logger.error(
                f"Erro na background task de prioridade da Tarefa {task_id}: {e}"
            )

    async def _persist_background_priority(
        self, task_id: int, new_priority: str
    ) -> None:
        """
        Helper privado responsável por gerenciar a injeção da sessão isolada em background.
        Mantém o SRP: a rotina de IA sugere, este helper persiste.
        """
        async with self.bg_repo_factory() as bg_repo:
            await bg_repo.update_task_priority(task_id, new_priority)
        logger.info(
            f"Prioridade da Tarefa {task_id} atualizada assincronamente para: {new_priority}"
        )

    async def get_task(self, task_id: int) -> TaskResponse | None:
        """
        Busca os detalhes de uma tarefa pontual pelo ID.

        Args:
            task_id (int): ID identificador da tarefa.

        Returns:
            TaskResponse | None: DTO da tarefa encontrada ou None se não existir.
        """
        return await self.repo.get_task(task_id)

    async def get_tasks(
        self, is_completed: bool | None = None, priority: str | None = None
    ) -> list[TaskResponse]:
        """
        Lista as tarefas ativas, aplicando os filtros opcionais.

        Args:
            is_completed (bool | None, optional): Filtra pelo status de conclusão. Defaults to None.
            priority (str | None, optional): Filtra pelo nível de prioridade. Defaults to None.

        Returns:
            list[TaskResponse]: Lista contendo as tarefas encontradas.
        """
        return await self.repo.get_tasks(is_completed=is_completed, priority=priority)

    async def update_task(
        self, task_id: int, task_update: TaskUpdate
    ) -> TaskResponse | None:
        """
        Atualiza os dados de uma tarefa existente aplicando uma atualização parcial (PATCH).

        Args:
            task_id (int): ID identificador da tarefa.
            task_update (TaskUpdate): DTO contendo os campos opcionais a serem modificados.

        Returns:
            TaskResponse | None: DTO da tarefa atualizada ou None se não existir.
        """
        # Converte o schema Pydantic em um dicionário, excluindo campos não enviados
        update_data = task_update.model_dump(exclude_unset=True)

        if not update_data:
            # Se nenhum dado for enviado, retorna o estado atual sem fazer alterações
            return await self.repo.get_task(task_id)

        return await self.repo.update_task(task_id, update_data)

    async def delete_task(self, task_id: int) -> bool:
        """
        Deleta uma tarefa permanentemente.

        Args:
            task_id (int): ID identificador da tarefa.

        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso não tenha encontrado o registro.
        """
        return await self.repo.delete_task(task_id)
