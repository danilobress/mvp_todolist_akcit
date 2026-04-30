import logging
import httpx

from app.schemas.task import TaskPriority
from app.config import settings

logger = logging.getLogger(__name__)

class PriorityAdvisorClient:
    """
    Cliente para integração com serviço de LLM externo (IA) responsável por 
    sugerir a prioridade de uma tarefa. Implementa resiliência de rede e 
    tratamento de alucinações.
    """

    def __init__(self, client: httpx.AsyncClient):
        """
        Inicializa o cliente com injeção de dependência e carrega credenciais.
        
        Args:
            client (httpx.AsyncClient): Sessão HTTP assíncrona compartilhada.
        """
        self.client = client
        # Carrega as configurações validadas pelo Pydantic Settings
        self.api_url = settings.llm_api_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model

    async def suggest_priority(self, title: str, description: str | None) -> TaskPriority:
        """
        Envia os dados da tarefa para o LLM analisar e inferir a prioridade.
        Aplica fallback silencioso ("Média") em caso de indisponibilidade de rede, 
        timeout, erro de autenticação ou se o modelo retornar respostas inválidas.
        
        Args:
            title (str): Título da tarefa.
            description (str | None): Descrição detalhada (opcional).
            
        Returns:
            TaskPriority: TaskPriority.ALTA, TaskPriority.MEDIA ou TaskPriority.BAIXA.
        """
        if not self.api_key:
            logger.warning(f"LLM_API_KEY não configurada. Aplicando fallback silencioso '{TaskPriority.MEDIA.value}'.")
            return TaskPriority.MEDIA

        # System prompt rigoroso focado em retornar apenas as palavras permitidas
        system_prompt = (
            "Você é um classificador de prioridade de tarefas. "
            "Sua única função é analisar o título e a descrição de uma tarefa e "
            "retornar ESTRITAMENTE UMA DAS TRÊS PALAVRAS a seguir, sem pontuação "
            "ou explicações adicionais: Alta, Média, ou Baixa."
        )
        
        user_content = f"Título: {title}\n"
        if description:
            user_content += f"Descrição: {description}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.1 # Leve aumento para evitar travamento da IA no wrapper
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            # Aumentando levemente o timeout caso a IA precise pensar um pouco mais
            response = await self.client.post(
                self.api_url, 
                json=payload, 
                headers=headers, 
                timeout=5.0
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Garantindo que extrairemos a string mesmo se a estrutura mudar levemente
            try:
                raw_answer = data["choices"][0]["message"]["content"]
                if raw_answer is None:
                    raw_answer = ""
            except (KeyError, IndexError):
                raw_answer = ""
            
            # Limpeza profunda contra alucinações (espaços, pontos, quebras de linha e case)
            clean_answer = raw_answer.strip().strip('.').capitalize()
            
            valid_priorities = {p.value for p in TaskPriority}
            
            if clean_answer in valid_priorities:
                return TaskPriority(clean_answer)
            else:
                logger.warning(f"LLM não retornou a prioridade esperada.\nConteúdo limpo: '{clean_answer}'\nResposta completa da API: {data}\nFallback para '{TaskPriority.MEDIA.value}'.")
                return TaskPriority.MEDIA

        except httpx.TimeoutException as e:
            logger.warning(f"Timeout ao conectar no LLM ({e}). Fallback silencioso para '{TaskPriority.MEDIA.value}'.")
            return TaskPriority.MEDIA
        except httpx.HTTPStatusError as e:
            # Captura erros como 401 Unauthorized ou 403 Forbidden
            logger.warning(f"Erro HTTP do LLM ({e.response.status_code}). Fallback silencioso para '{TaskPriority.MEDIA.value}'.")
            return TaskPriority.MEDIA
        except httpx.RequestError as e:
            logger.warning(f"Falha de rede ao acessar LLM ({e}). Fallback silencioso para '{TaskPriority.MEDIA.value}'.")
            return TaskPriority.MEDIA
        except Exception as e:
            logger.error(f"Erro inesperado no PriorityAdvisor ({e}). Fallback silencioso para '{TaskPriority.MEDIA.value}'.")
            return TaskPriority.MEDIA
