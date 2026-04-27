from datetime import datetime, timezone
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

# Instanciação da aplicação com metadados
app = FastAPI(
    title="API do Gerenciador de Tarefas PriorityAdvisor",
    description="Uma API minimalista para gerenciar tarefas com sugestões de prioridade baseadas em IA.",
    version="1.0.0",
)

class HealthCheckResponse(BaseModel):
    """Modelo Pydantic para a resposta de verificação de integridade (health check).

    Atributos:
        status (str): O status atual da API.
        timestamp (datetime): O carimbo de data/hora UTC atual.
    """
    status: str = Field(..., description="O status operacional atual da API")
    timestamp: datetime = Field(..., description="O carimbo de data/hora UTC da verificação de integridade")

@app.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Executar uma verificação de integridade",
    description="Endpoint usado para verificar se a API está funcionando corretamente.",
    tags=["Monitoramento"],
)
def health_check() -> HealthCheckResponse:
    """Lida com a solicitação de verificação de integridade.

    Returns:
        HealthCheckResponse: Uma resposta estruturada contendo o status da API e o horário UTC atual.
    """
    return HealthCheckResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc)
    )
