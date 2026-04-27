# 📋 Gerenciador de Tarefas (MVP)

API RESTful minimalista e resiliente para gerenciamento de tarefas (To-Do List), potencializada por Inteligência Artificial para sugestão automática de prioridades.

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.12+
* **Framework Web:** FastAPI
* **Servidor ASGI:** Uvicorn
* **ORM e Banco de Dados:** SQLAlchemy & SQLite (Embutido)
* **Validação de Dados:** Pydantic
* **Testes & QA:** Pytest, HTTPX, pytest-asyncio, RESPX (Mocking)

## 🏗️ Arquitetura do Sistema

O projeto adota rigorosamente o padrão arquitetural **Controller-Service-Repository**, garantindo separação de responsabilidades (SRP), alta testabilidade e baixo acoplamento:

* **Controller (Routers/Endpoints):** Camada de apresentação da API (`app.main` e roteadores). Responsável exclusivamente por receber requisições HTTP, validar payloads de entrada via Pydantic e retornar respostas HTTP apropriadas. Não contém regras de negócio.
* **Service (Lógica de Negócio):** O cérebro da aplicação. Orquestra as validações complexas, integra-se com serviços externos (como o `PriorityAdvisor` para IA) e coordena o fluxo de dados. Totalmente agnóstico em relação a banco de dados ou frameworks web pesados.
* **Repository (Acesso a Dados):** Camada de persistência puramente dedicada à interação com o SQLAlchemy. Isola o banco de dados (SQLite) da lógica de negócio. Não toma decisões de negócio nem levanta exceções HTTP.

*Decisão de Design:* O uso do SQLite foi escolhido intencionalmente para maximizar a portabilidade e simplicidade do MVP, dispensando infraestrutura externa. A camada Repository garante que uma futura migração para PostgreSQL exija mudanças isoladas.

## 🚀 Como Executar (Ambiente de Desenvolvimento)

Siga os passos abaixo para configurar o ambiente local do zero. Não é necessário Docker ou banco de dados externo.

1. **Clone o repositório e acesse o diretório:**
   ```bash
   git clone <url-do-repositorio>
   cd gerenciador_tarefas
   ```

2. **Crie e ative o ambiente virtual (venv):**
   ```bash
   # Linux/macOS
   python3.12 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Instale as dependências (incluindo ferramentas de desenvolvimento/teste):**
   ```bash
   pip install -e ".[dev]"
   ```
   *(Nota: Caso o projeto utilize `requirements.txt` temporariamente, execute `pip install -r requirements.txt`)*

4. **Inicie o servidor de desenvolvimento:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   A API estará disponível em: `http://localhost:8000`
   A documentação interativa (Swagger UI) em: `http://localhost:8000/docs`

## 🧪 Suíte de Testes (QA)

A meta de qualidade exige 100% de cobertura nos fluxos críticos. A suíte de testes foi projetada para ser rápida, determinística e isolada.

### Estratégia de Testes

* **Banco de Dados em Memória:** Os testes utilizam o recurso de *Dependency Overrides* do FastAPI para substituir a sessão de banco de dados real por um banco SQLite puramente em memória (`sqlite:///:memory:`). Isso garante isolamento total entre os testes e execução ultrarrápida.
* **Mock de Integrações Externas (IA):** Chamadas de rede para a API de LLM (PriorityAdvisor) são interceptadas e mockadas utilizando a biblioteca `respx` em conjunto com `httpx`. A rede externa nunca é acessada durante os testes automatizados.

### Executando os Testes

Para rodar a suíte completa com relatório de cobertura:

```bash
pytest --cov=app --cov-report=term-missing
```

## 🗺️ Roadmap de Releases

| Release | Foco | Objetivos Principais | Status |
| :--- | :--- | :--- | :--- |
| **v1.0 - Backend** | Estrutura & Persistência | Setup base, CRUD de Tarefas, isolamento Controller/Service/Repository, integração inicial com SQLite local e Integração real e heurística do `PriorityAdvisor`. | ⏳ Em Progresso |
| **v1.1 - Qualidade** | Cobertura de Testes | Setup do Pytest, mocks com `respx` e testes do banco em memória. | 📝 Planejado |
| **v1.2 - Entrega Final** | Polimento & Documentação | Refatoração final, garantia de tipagem estrita, revisão de Clean Architecture, README final e release do MVP. | 📝 Planejado |

## 🚫 Fora de Escopo (Escopo Negativo)

Para alinhar expectativas e focar estritamente nos objetivos do MVP, os seguintes itens **NÃO** fazem parte desta entrega:

* **Frontend/GUI:** Nenhuma interface gráfica (Web, Mobile ou Desktop) será desenvolvida. A interação é exclusivamente via API REST.
* **Infraestrutura e Nuvem (Cloud/Docker):** O projeto foi desenhado para rodar localmente via `uvicorn`. Deployments em nuvem, orquestração com Docker/Kubernetes ou CI/CD pipelines estão fora do escopo.
* **Bancos de Dados Externos:** Não há suporte ou scripts de migração para PostgreSQL, MySQL ou bancos NoSQL nesta fase. O SQLite atende plenamente os requisitos de persistência local.
* **Autenticação e Autorização:** Sistemas de login, tokens JWT, OAuth ou gestão de usuários e papéis (RBAC) não estão contemplados. A API é aberta por design para simplificar o MVP.
