from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel):
    """
    Schema estrito para a criação de uma nova tarefa.
    Valida apenas os dados iniciais fornecidos pelo usuário.
    """
    title: str = Field(..., max_length=100, description="Título principal da tarefa")
    description: str | None = Field(default=None, max_length=500, description="Descrição detalhada da tarefa")

class TaskUpdate(BaseModel):
    """
    Schema para a atualização parcial de uma tarefa (PATCH).
    Permite alterar título, descrição, status de conclusão e prioridade.
    """
    title: str | None = Field(default=None, max_length=100, description="Título principal da tarefa")
    description: str | None = Field(default=None, max_length=500, description="Descrição detalhada da tarefa")
    is_completed: bool | None = Field(default=None, description="Status de conclusão da tarefa")
    priority: str | None = Field(default=None, description="Nível de prioridade (ex: Alta, Média, Baixa)")

class TaskResponse(BaseModel):
    """
    Schema para a representação de saída de uma tarefa.
    """
    id: int
    title: str
    description: str | None
    is_completed: bool
    priority: str

    model_config = ConfigDict(from_attributes=True)
