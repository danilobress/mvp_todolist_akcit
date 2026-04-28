# Gerenciador de Tarefas (MVP)

## Visão Geral do Projeto
Este projeto é um MVP (Minimum Viable Product - Produto Mínimo Viável) para um aplicativo de Gerenciamento de Tarefas (Lista de Tarefas ou To-Do List). Atualmente consiste em uma API backend assíncrona e modular construída com Python e FastAPI, utilizando um banco de dados SQLite local para persistência e integração com IA (PriorityAdvisor) para sugestão automática de prioridade.

O backend segue estritamente um padrão arquitetural de 3 camadas:
1. **Models (Domínio e Validação)**: Define a "forma" da informação. Contém as entidades do banco de dados (SQLAlchemy) e os contratos de dados/DTOs (Pydantic).
2. **Services**: O cérebro da aplicação. Contém a lógica de negócios central, orquestração de regras e integrações com serviços externos.
3. **Repositories**: Camada de acesso a dados isolada, responsável por interagir exclusivamente com o banco de dados SQLite.

## Regras de Interação para a Inteligência Artificial (Gemini)
- **Código Completo:** NUNCA gere códigos com placeholders como `# sua lógica aqui` ou `...`. Escreva a implementação completa da função solicitada.
- **Respostas Diretas:** Ao ser solicitado a refatorar ou criar um arquivo, foque no código. Evite longas introduções a menos que seja pedido para explicar um conceito.
- **Contexto de Arquivo:** Sempre verifique a estrutura de pastas antes de sugerir o caminho de importação (import statements) dos módulos.

## Principais Tecnologias
- **Backend**
  - **Linguagem**: Python >= 3.12
  - **Framework**: FastAPI
  - **Servidor**: Uvicorn
  - **ORM**: SQLAlchemy
  - **Validação de Dados**: Pydantic
  - **Banco de Dados**: SQLite (Local)
  - **Inteligência Artificial**: PriorityAdvisor (Sugestão de Prioridades)
  - **Testes**: Pytest, httpx, pytest-asyncio, respx

## Estrutura do Projeto
- `/docs/`: Contém a documentação do projeto, incluindo escopo (`escopo-mvp.md`), backlog (`backlog.md`) e diagramas arquiteturais (`arquitetura.mmd`).
- `/prompts/`: Prompts de engenharia de IA baseados no modelo CO-STAR.
- `/backend/`: Código fonte da API (contém `app/main.py`, `app/services/task_services`, `app/repositories/task_repository`, `app/models/task.py`, `app/schemas` e app/backend).
- `pyproject.toml`: Define os metadados do projeto, dependências e configurações de build.

## Construção e Execução

### Configuração do Ambiente
O projeto usa um ambiente virtual Python padrão (`.venv`).
```bash
# Ativar o ambiente virtual (Windows)
.\.venv\Scripts\activate

# Instalar dependências (incluindo ferramentas de desenvolvimento)
pip install -r requirements.txt
```

### Executando a Aplicação
Assumindo que a aplicação FastAPI principal será criada em `main.py`:
```bash
uvicorn main:app --reload
```
*(Nota: Arquivos de código-fonte como `main.py` devem ser implementados conforme o backlog.)*

### Testes
Os testes são executados usando Pytest:
```bash
pytest
```

## Convenções e Diretrizes de Desenvolvimento Backend
- **Estilo de Código**: Adesão estrita à PEP 8.
- **CORS Obligatório**: O FastAPI deve estar configurado com `CORSMiddleware` para liberar acesso às origens necessárias.
- **Tipagem**: O uso de type hinting explícito é obrigatório em todas as funções. Retornos de API devem usar schemas Pydantic.
- **Banco de Dados**: Devido às limitações do SQLite, use `check_same_thread=False` na conexão.
- **Requisitos de Teste**: 
  - Forneça testes cobrindo as seguintes frentes: Camada de Service, PriorityAdvisor, Integração (API/Banco de Dados) e Repositório.
  - Testes de API devem ser isolados usando `pytest` e `TestClient` (httpx).
  - Use `Dependency Overrides` no FastAPI para substituir a conexão do banco por um SQLite em memória durante os testes (`sqlite:///:memory:`). OBRIGATORIAMENTE configure a *engine* de testes com `poolclass=StaticPool` para evitar conflitos de escopo transacional.
  - Utilize a biblioteca `respx` OBRIGATORIAMENTE para mockar as chamadas HTTP de serviços externos, como o PriorityAdvisor.
  - Nos testes da camada de Service, faça mock do Repository e abstraia chamadas externas.

## Versionamento (Git)
- **Conventional Commits**: Ao sugerir comandos ou mensagens de commit, utilize obrigatoriamente o padrão Conventional Commits. Use o português Brasil para as mensagens de commit.
  - `feat:` para novas funcionalidades (ex: novos endpoints ou componentes).
  - `fix:` para correção de bugs.
  - `refactor:` para melhorias de código sem adição de feature.
  - `test:` para adição ou correção de testes (Pytest/Vitest).
  - `chore:` para atualizações de dependências ou configurações (ex: setup do pytest).
  - `docs:` para alterações no README ou escopo.

## Diretrizes de Documentação de Código
- **Backend (Python)**: Use obrigatoriamente o padrão **Google Style Docstrings**. 
  - Toda função em `services` e `repositories` deve documentar Args, Returns e Raises.
  - Especifique claramente `Args`, `Returns` e mapeie possíveis erros em `Raises`.
  - Funções privadas ou auxiliares (iniciadas com `_`, ex: `_format_date`) não precisam de docstrings exaustivas.

## Restrições de Escopo (MVP)
Exclua explicitamente a criação de autenticação (JWT/Login), deploys em nuvem (Docker/AWS) e bancos relacionais robustos (PostgreSQL). Mantenha tudo rodando localmente. (PostgreSQL). Mantenha tudo rodando localmente.