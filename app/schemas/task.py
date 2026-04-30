from typing import Literal
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator

class TaskPriority(str, Enum):
    ALTA = "Alta"
    MEDIA = "Média"
    BAIXA = "Baixa"

class TaskCreate(BaseModel):
    """
    Schema estrito para a criação de uma nova tarefa.
    Valida apenas os dados iniciais fornecidos pelo usuário.
    """
    model_config = ConfigDict(extra="forbid")
    
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
    priority: TaskPriority | None = Field(default=None, description="Nível de prioridade (ex: Alta, Média, Baixa)")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str | None) -> str | None:
        if v is None:
            raise ValueError("O título não pode ser nulo")
        if not v.strip():
            raise ValueError("O título não pode estar em branco")
        return v

class TaskResponse(BaseModel):
    """
    Schema para a representação de saída de uma tarefa.
    """
    id: int
    title: str
    description: str | None
    is_completed: bool
    priority: TaskPriority

    model_config = ConfigDict(from_attributes=True)
