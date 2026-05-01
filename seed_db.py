import asyncio
import sys
import os

# Adiciona o diretório atual ao path para garantir que a pasta app seja encontrada
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import engine, async_session_maker
from app.models.task import Base
from app.schemas.task import TaskCreate, TaskPriority
from app.repositories.task_repository import TaskRepository


async def seed_data():
    """
    Script para popular o banco de dados local SQLite com dados iniciais (Seed).
    Utiliza estritamente a nova arquitetura assíncrona (aiosqlite) e as injeções de dependência manuais.
    """
    print("Inicializando criação do banco de dados assíncrono...")

    # 1. Cria as tabelas no banco de dados (SQLite local via aiosqlite)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Inicializa as dependências de banco de dados
    async with async_session_maker() as db_session:
        try:
            repo = TaskRepository(db_session)

            # Verifica se já existem tarefas
            existing_tasks = await repo.get_tasks()
            if len(existing_tasks) > 0:
                print(
                    f"O banco de dados já contém {len(existing_tasks)} tarefas. Nenhuma nova tarefa foi adicionada."
                )
                return

            print("Populando o banco de dados com tarefas iniciais do MVP...")

            tarefas_iniciais = [
                TaskCreate(
                    title="Configurar ambiente de desenvolvimento",
                    description="Instalar Python, Node.js e configurar a IDE para o projeto MVP.",
                ),
                TaskCreate(
                    title="Implementar backend com FastAPI",
                    description="Criar as rotas, models e conexão com SQLite assíncrona.",
                ),
                TaskCreate(
                    title="Criar repositório Git",
                    description="Inicializar o git e fazer o primeiro commit com a estrutura base.",
                ),
                TaskCreate(
                    title="Escrever Suíte de Testes (QA)",
                    description="Criar os testes automatizados com Pytest e respx.",
                ),
            ]

            created_tasks = []
            for tarefa in tarefas_iniciais:
                # Inserção direta via repositório para ignorar a execução da IA no ambiente de Seed
                created_task = await repo.create_task(
                    tarefa, initial_priority=TaskPriority.MEDIA.value
                )
                created_tasks.append(created_task)
                print(
                    f"Tarefa persistida: {created_task.title} (ID: {created_task.id}) - Prioridade: {created_task.priority}"
                )

            # Marca a primeira tarefa como concluída para variedade de dados
            if created_tasks:
                primeira_tarefa_id = created_tasks[0].id
                await repo.update_task(primeira_tarefa_id, {"is_completed": True})
                print(f"-> Tarefa ID {primeira_tarefa_id} marcada como concluída.")

            print("Banco de dados populado com sucesso!")

        except Exception as e:
            print(f"Erro ao popular o banco: {e}")


if __name__ == "__main__":
    # Roda o script de forma assíncrona utilizando a biblioteca asyncio nativa do Python
    asyncio.run(seed_data())
