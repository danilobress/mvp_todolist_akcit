# Product Backlog: Gerenciador de Tarefas (MVP)

## Release 1: Core Backend (CRUD & PriorityAdvisor)

- [ ] 1.1 **Configuração Inicial do Projeto e Banco de Dados**
  - **Descrição:** Configurar o FastAPI, estrutura de pastas e conexão assíncrona com SQLite, respeitando a separação de responsabilidades.
  - **Critérios de Aceite:**
    - Arquitetura de 3 camadas (Models/Schemas, Services, Repositories) definida estruturalmente.
    - Conexão SQLAlchemy com SQLite local configurada obrigatoriamente de forma assíncrona (utilizando o driver `aiosqlite` e `sqlalchemy.ext.asyncio`) para mitigar *database locks*.
    - Tabela de tarefas mapeada via SQLAlchemy gerada automaticamente na inicialização.

- [ ] 1.2 **Implementação do Domínio (Models e Schemas)**
  - **Descrição:** Criar os modelos de persistência (SQLAlchemy) e contratos de dados/DTOs (Pydantic) para validação.
  - **Critérios de Aceite:**
    - Modelo SQLAlchemy `Task` com os atributos definidos pelo negócio.
    - Schemas Pydantic (`TaskCreate`, `TaskUpdate`, `TaskResponse`) criados.
    - Validação estrita via Pydantic garantindo o retorno do HTTP status `422 Unprocessable Entity` em caso de requisição inválida.

- [ ] 1.3 **Endpoint: Criação de Tarefas (POST /tasks)**
  - **Descrição:** Desenvolver fluxo Controller -> Service -> Repository para inserção de tarefas. Integrar com o serviço PriorityAdvisor via Background Task para inferência de prioridade caso omitida.
  - **Critérios de Aceite:**
    - Retorno com HTTP status `201 Created` contendo o payload `TaskResponse`.
    - O Service atribui a prioridade padrão "Média" no instante da criação e agenda o PriorityAdvisor via `FastAPI BackgroundTasks` se a prioridade não for informada no input.
    - O cliente `httpx` deve ter limites de *timeout* estritos (1 a 2 segundos) e prever blocos `try/except` para falhas de rede.
    - Persistência delegada e isolada rigorosamente ao `TaskRepository`.

- [ ] 1.4 **Endpoint: Listagem de Tarefas (GET /tasks)**
  - **Descrição:** Rota para a recuperação em lote das tarefas armazenadas no banco local.
  - **Critérios de Aceite:**
    - Retorno com HTTP status `200 OK` apresentando um array do tipo `TaskResponse`.
    - Suporte a filtros opcionais via *query parameters* (`is_completed`, `priority`) validados via dependências do FastAPI e integrados na consulta dinâmica do SQLAlchemy.
    - Retorno de um array vazio `[]` (com status `200`) na ausência de registros ou se nenhum registro corresponder aos filtros.
    - Acesso à base de dados exclusivamente orquestrado pelo `TaskRepository`.

- [ ] 1.5 **Endpoint: Consulta de Tarefa Específica (GET /tasks/{task_id})**
  - **Descrição:** Rota para a busca pontual dos detalhes de uma tarefa baseada em seu ID único.
  - **Critérios de Aceite:**
    - Retorno com HTTP status `200 OK` entregando o objeto `TaskResponse` esperado.
    - Retorno com HTTP status `404 Not Found` caso o ID informado não corresponda a nenhum registro no banco.

- [ ] 1.6 **Endpoint: Atualização de Tarefas (PATCH /tasks/{task_id})**
  - **Descrição:** Rota para modificar atributos de uma tarefa preexistente.
  - **Critérios de Aceite:**
    - Validação completa do payload via esquema `TaskUpdate`, com HTTP status `422 Unprocessable Entity` para anomalias de entrada.
    - Retorno com HTTP status `200 OK` contendo a representação atualizada da entidade em caso de sucesso.
    - Retorno com HTTP status `404 Not Found` para requisições em que a tarefa não exista no sistema.

- [ ] 1.7 **Endpoint: Exclusão de Tarefas (DELETE /tasks/{task_id})**
  - **Descrição:** Remoção definitiva do registro de uma tarefa do sistema através do seu ID.
  - **Critérios de Aceite:**
    - Sucesso sinalizado exclusivamente via HTTP status `204 No Content` sem corpo de resposta.
    - Requisições visando IDs inativos/inexistentes devem disparar a resposta HTTP status `404 Not Found`.

## Release 2: Qualidade (Testes Automatizados)

- [ ] 2.1 **Setup do Ambiente e Base em Memória para Testes**
  - **Descrição:** Preparar o Pytest e o FastAPI para a execução robusta de testes isolados e reproduzíveis.
  - **Critérios de Aceite:**
    - Plugin `pytest-asyncio` devidamente ativo no ambiente.
    - Substituição inteligente de dependências (`Dependency Overrides`) na instância do FastAPI para conectar uma base SQLite transiente (`sqlite:///:memory:`) configurada com `poolclass=StaticPool` para garantir uma única conexão global.
    - Fixtures (de setup/teardown) que garantam esquemas limpos para cada teste individual executado.

- [ ] 2.2 **Testes de Repositório (Integração com Banco de Dados)**
  - **Descrição:** Validar as operações de CRUD diretamente na camada de repositório, garantindo que as queries SQLAlchemy funcionam conforme o esperado em uma base de testes.
  - **Critérios de Aceite:**
    - Testes para inserção, busca por ID, listagem, atualização e deleção utilizando o SQLite em memória.
    - Garantia de que exceções do banco de dados (se houver) são tratadas ou propagadas corretamente.

- [ ] 2.3 **Testes do PriorityAdvisor e Integrações Externas**
  - **Descrição:** Garantir que o cliente que consome a IA (PriorityAdvisor) funciona corretamente, isolando chamadas de rede.
  - **Critérios de Aceite:**
    - Uso da biblioteca `respx` para mockar as chamadas HTTP (via `httpx`) para o serviço de IA.
    - Validação dos cenários de sucesso (IA retorna prioridade válida) e cenários de falha (IA indisponível, timeout ou resposta malformada), garantindo fallback adequado (se aplicável).
    - Ausência de chamadas de rede reais durante a execução da suíte.

- [ ] 2.4 **Testes da Camada de Service**
  - **Descrição:** Validar a lógica de negócios da aplicação, orquestrando as regras independentemente do banco de dados e da API web.
  - **Critérios de Aceite:**
    - Uso de mocks (ex: `unittest.mock` ou `pytest-mock`) para a camada de `Repository` e para o cliente do `PriorityAdvisor`, garantindo que ambos sejam injetados via construtor na instância do Service para permitir testabilidade confiável via `respx`. Os mocks do Repositório devem retornar estritamente DTOs Pydantic.
    - Validação das regras de negócio (ex: chamada ao PriorityAdvisor apenas quando a prioridade é omitida na criação).
    - Testes verificando o levantamento de exceções apropriadas (ex: exceções de negócio ou delegação do 404) quando regras de negócio falham.

- [ ] 2.5 **Testes de Integração (API / Banco de Dados)**
  - **Descrição:** Validar o fluxo completo de ponta a ponta (Controller -> Service -> Repository) utilizando o `TestClient`.
  - **Critérios de Aceite:**
    - Cobertura de sucesso (happy paths) confirmando respostas HTTP `200`, `201` e `204`.
    - Casos extremos testados ativamente (bad paths), verificando assertivamente ocorrências de HTTP status `404` e `422`.
    - Mocks de rede via `respx` aplicados no fluxo de API para que o PriorityAdvisor não seja chamado de fato externamente.

## Release 3: Entrega Final (Handoff Interno)

- [ ] 3.1 **Polimento Técnico e Padrões de Documentação**
  - **Descrição:** Refatorações cirúrgicas garantindo aderência absoluta aos padrões arquiteturais do MVP e segurança.
  - **Critérios de Aceite:**
    - Documentação inline preenchida e aderente ao `Google Style Docstrings` focada nos `Services` e `Repositories` (com Args, Returns e Raises explícitos).
    - Código com forte Type Hinting validado em 100% de seus escopos públicos.
    - Garantia que o `CORSMiddleware` esteja habilitado corretamente na instância do FastAPI principal.
    - Ausência de infraestrutura em nuvem, Docker, PostgreSQL, sistemas de login/autenticação ou notificações (escopo negativo respeitado).

- [ ] 3.2 **Finalização do Guia Rápido (README e Inicialização)**
  - **Descrição:** Empacotar e preparar o roteiro para o próximo desenvolvedor conseguir consumir o MVP a frio.
  - **Critérios de Aceite:**
    - O processo de inicialização de virtual environment (.venv) e instalação (`pip install -r requirements.txt`) claro e documentado.
    - O comando de run do Uvicorn explicitado.
    - Comandos de run do pytest registrados para facilitar a testabilidade sob demanda.s para facilitar a testabilidade sob demanda.