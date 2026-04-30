## Criando .gitignore
```
Atue como um Arquiteto de Software Sênior 
Contexto: Estou iniciando a arquitetura de um MVP utilizando Python e FastAPI, estruturado com o padrão de repositório para a entidade "Produto". O ecossistema do projeto incluirá integração com banco de dados relacional e uma camada rigorosa de automação de testes.
Objetivo: Gere um arquivo .gitignore de nível de produção para este repositório. Ele deve garantir que código-fonte limpo seja rastreado, bloqueando artefatos de compilação, ambientes virtuais, caches de frameworks de teste e configurações locais.
Estilo: Organize o conteúdo estritamente por seções lógicas, utilizando comentários em inglês para padronização (ex: # Python Core, # Virtual Environments, # Testing & QA, # IDEs & OS).
Tom: Técnico, autoritário e focado em segurança de dados (prevenção contra vazamento de variáveis de ambiente).
Público: Engenheiros de software e especialistas em qualidade (QA) que clonarão e trabalharão neste repositório.
Resposta: crie um arquivo .gitignore de nível de produção para este repositório de código. Não inclua saudações, explicações adicionais ou textos de encerramento.
Restrições: Certifique-se de incluir regras específicas para o framework de testes (como .pytest_cache, .coverage), ferramentas de automação, arquivos de configuração de banco de dados locais, variáveis de ambiente (como .env) e pastas de IDEs comuns (como .vscode/ e .idea/).
```

## Escopo MVP

```
Atue como um Analista de Requisitos Sênior e Engenheiro de Qualidade (QA).
Contexto: Estamos desenvolvendo um MVP de uma Micro-API de Gerenciamento de Tarefas (To-Do List) com um limite estrito de 30 horas de desenvolvimento. A stack tecnológica definida é Python 3.12 com FastAPI no backend estruturada no padrão Controller-Service-Repository, banco de dados local SQLite.

Objetivo: Elaborar o documento fundacional de escopo do projeto. O documento deve definir claramente:

1. O objetivo principal do MVP.
2. Requisitos Funcionais (operações CRUD detalhadas para a entidade "Task" permitindo criar, editar, deletar e listar as tarefas, filtrar essas tarefas por status de conclusão e prioridade, e usar o PriorityAdvisor (AI) para sugerir automaticamente a prioridade da tarefa).
3. Requisitos Não Funcionais (desempenho, persistência de dados local isolada no Repository, testabilidade com Pytest, pytest-asyncio e respx para mocks).
4. O que está explicitamente "Fora de Escopo" (ex: autenticação, deploy em nuvem, banco de dados complexo).

Estilo: Escrita técnica de engenharia de software. Estruture a informação usando listas, tópicos e tabelas onde for necessário para facilitar a escaneabilidade.
Tom: Profissional, direto, pragmático e focado na entrega de valor e simplicidade.
Público: Desenvolvedores e profissionais de teste de software que usarão este documento como guia definitivo para codificar e criar os casos de teste do MVP.
Resposta: Crie o arquivo 'docs/escopo-mvp.md' e gere dentro desse arquivo o código fonte em Markdown (.md). Não inclua saudações, conclusões ou textos explicativos fora do bloco de código Markdown.
```

## Release Backlog

```
Atue como um Agile Coach e Arquiteto de Software Sênior
Contexto: O projeto é um MVP de gerenciamento de tarefas com backend assíncrono em FastAPI (arquitetura modular estrita com Controller, Services e Repositories). O ciclo de vida do produto foi fatiado em 3 releases estratégicas:

Core Backend: Implementação de um CRUD básico, persistência em SQLite isolada no Repository e PriorityAdvisor (AI) para sugerir automaticamente a prioridade da tarefa na camada de Service.

Qualidade: Criação dos testes unitários e de integração (Pytest, pytest-asyncio, httpx e respx para mocks da IA). Testes da Camada de Service, Testes do PriorityAdvisor, Testes de Integração (API / Banco de Dados) e Testes de Repositório (Integração com Banco de Dados)

Entrega Final: Pronto para Handoff Interno.

Objetivo: Crie um Product Backlog enxuto e acionável. Converta os requisitos do Documento de Escopo em tarefas claras, mapeando as dependências. Cada tarefa deve obrigatoriamente possuir Critérios de Aceite bem definidos (preferencialmente usando uma lógica clara de validação de cenários de sucesso e erro).
Estilo: Documento Markdown formatado primariamente como um checklist iterável (- [ ]), hierarquizado em seções para cada uma das 3 releases.
Tom: Técnico, pragmático e orientado a entregáveis de alto valor agregado.
Público: Desenvolvedores e Engenheiros de Qualidade (QA) que consumirão este documento para planejar e executar a sprint.
Resposta: Crie o arquivo docs/backlog.md e gere dentro desse arquivo o código fonte em Markdown (.md). Oculte qualquer saudação, explicação sobre o método ou texto de encerramento.
Restrições: Nenhuma tarefa deve mencionar itens de infraestrutura em nuvem, Docker, PostgreSQL, sistemas de login/autenticação ou notificações. O escopo negativo deve ser rigorosamente respeitado.
Critérios de Aceite: Certifique-se de que as tarefas de backend mencionem as validações Pydantic e os códigos HTTP esperados (200, 201, 204, 404, 422). As tarefas de Qualidade devem exigir isolamento de banco de dados e mock de rede externa.
```

## Diagrama de Fluxo Mermaid

```
Atue como um Arquiteto de Software Sênior
Contexto: O projeto é um MVP de Gerenciamento de Tarefas (To-Do List). A arquitetura é composta por um Backend síncrono/assíncrono em Python (FastAPI). O backend está estruturado estritamente em três camadas lógicas: Controller (Routers/Endpoints), Services (Regras de Negócio) e Repositories (Acesso a Dados). A persistência é feita localmente com SQLite.
Objetivo: Gere um diagrama arquitetural e de fluxo de dados utilizando a sintaxe Mermaid.js. O diagrama deve mapear visualmente a topologia do sistema e o fluxo de uma requisição típica de CRUD (ex: Criar Tarefa) até a persistência no banco de dados, incluindo a integração com o PriorityAdvisor (AI).
Estilo: Utilize um grafo direcionado (ex: graph TD ou graph LR). Organize a estrutura utilizando nós e subgraph para delimitar claramente as fronteiras do sistema: Backend (FastAPI) e Database. As setas devem ser rotuladas para indicar o tipo de comunicação ou fluxo de dados.
Tom: Técnico, direto e focado em documentação de engenharia de software pragmática.
Público: Desenvolvedores e engenheiros de QA que precisam de uma visão clara e versionável da arquitetura do projeto.
Resposta: Criei o arquivo em /docs/api-diagram.mmd com o bloco de código contendo o script Mermaid. Omita qualquer tipo de saudação, explicação sobre as decisões arquiteturais ou texto fora do bloco de código.
Restrições: Não inclua nós ou fluxos para sistemas de Autenticação (Login/Tokens), serviços em Nuvem (AWS, Docker, CI/CD), bancos de dados externos (PostgreSQL) ou integrações de terceiros.
Nível de Detalhe: Especifique as labels nas setas para demonstrar o contrato (ex: Service para Repository use Modelos Pydantic/Objetos, de Repository para SQLite use Queries SQL).
```

## Diagrama de Componente Mermaid

```
Atue como um Arquiteto de Software Sênior
Contexto: Precisamos documentar a "Visão de Componentes e Rotas" do nosso MVP (Backend FastAPI) utilizando a sintaxe do Mermaid.js.
Objetivo: Gere o código de um Diagrama de Fluxo (Flowchart `graph TD` ou `graph LR`) que mapeie os contratos expostos da API e a orquestração interna de serviços.
O diagrama deve refletir estritamente a seguinte estrutura:
1. **Foco em Usabilidade:** Ignore detalhes de persistência. Não inclua nós para SQLite, ORM, Pydantic ou banco de dados.
2. **Entrada:** Crie um nó representando o "Cliente HTTP / Consumidor".
3. **Controlador Central:** Crie um nó/subgrafo para a "API (FastAPI / main.py)".
4. **Mapeamento de Rotas:** Desenhe setas do Cliente para a API anotadas explicitamente com os endpoints reais: `GET /health`, as rotas base `/tasks` e a rota especializada `/tasks/priority:suggest`.
5. **Orquestração:** Desenhe o fluxo onde a API (main.py) repassa todas as requisições para o componente `TaskService`.
6. **Dependências do Service:** Mostre o `TaskService` ramificando e orquestrando as chamadas para os componentes isolados `TaskRepository` e `PriorityAdvisor (IA)`.

Estilo: Código Mermaid limpo. Utilize `subgraph` para delimitar o escopo do "Backend". Aplique estilos básicos (`classDef`) para destacar visualmente as rotas/setas de integração.
Tom: Estritamente técnico, documentacional e claro.
Público: Desenvolvedores e Engenheiros de QA que consumirão e testarão esses contratos de API.
Resposta: Criei o arquivo em /docs/component-diagram.mmd com o bloco de código contendo o script Mermaid. Omita qualquer tipo de saudação, explicação sobre as decisões arquiteturais ou texto fora do bloco de código.
Restrições: Não invente rotas ou componentes que não foram listados no Objetivo. O diagrama deve ser um reflexo fiel da Clean Architecture simplificada.
```

## Revisão de Planejamento

```
Atue como um Arquiteto de Software Sênior, Tech Lead e Agile Coach revisando o planejamento de uma sprint.
Contexto: Estou prestes a iniciar o desenvolvimento de um MVP de Gerenciamento de Tarefas (Backend FastAPI modular, Teste Unitário e Integração, banco SQLite local e e PriorityAdvisor (AI) para sugerir automaticamente a prioridade da tarefa na camada de Service). O projeto foi fatiado em 3 releases (Backend, Qualidade e Entrega Final). Abaixo, analise os arquivos /docs/escopo-mvp.md de escopo, /docs/backlog.md de backlog gerados, api-diagram.mmd e component-diagram.mmd

Objetivo: Realize uma análise crítica (sanity check) dos documentos fornecidos para identificar gargalos, falhas de planejamento e riscos arquiteturais antes do início da implementação. Responda estritamente a estas três perguntas:

Escopo: O que está grande demais ou complexo para a release inicial (Core) e deveria ser postergado?

Qualidade (QA): O que está faltando nos critérios de aceite ou na arquitetura descrita para garantir 100% de testabilidade (especialmente para os testes de integração com Pytest e httpx)?

Riscos: Quais são os 3 maiores riscos técnicos (arquiteturais ou de integração) que devo mitigar imediatamente?

Estilo: Respostas em bullet points curtos, diretos e acionáveis. Organize o texto utilizando as três perguntas como cabeçalhos (ex: ### 1. Ajustes de Escopo).
Tom: Analítico, pragmático, crítico e orientado à redução de riscos e eficiência de entrega.
Público: O time de desenvolvimento e QA que executará as tarefas.
Resposta: Forneça apenas a análise estruturada em Markdown. Omita saudações, conclusões genéricas ou explicações sobre a metodologia de análise.
Restrições: Baseie sua análise exclusivamente no texto fornecido. Lembre-se das restrições do projeto (sem nuvem, sem autenticação, uso estrito de SQLite).
```

## Criação README.md

```
Atue como um Arquiteto de Software Sênior.
Contexto: Estamos desenvolvendo um MVP de Gerenciamento de Tarefas (To-Do List) estritamente backend, focado em resiliência, testabilidade e integração com IA.

Backend: Python 3.12+, FastAPI, estruturado no padrão Controller-Service-Repository.
Persistência: SQLAlchemy com SQLite (decisão de design para simplicidade e portabilidade do MVP).
Integração IA: PriorityAdvisor (sugestão automática de prioridades usando IA e heurística local).
QA: Meta de 100% de cobertura em fluxos críticos usando Pytest, httpx, pytest-asyncio e respx (mock da IA).
Estratégia: Entrega dividida em 3 releases (Backend, Qualidade e Entrega Final).

Objetivo: Escreva o conteúdo completo do arquivo README.md. O documento deve ser o guia central do repositório, detalhando a visão técnica, como configurar o ambiente do zero e o progresso do desenvolvimento.
Estilo: Markdown profissional e técnico. Use ícones (emojis) discretos para categorizar seções, tabelas para o roadmap e blocos de código bem formatados. Organize a estrutura em:

- Título e Descrição curta (mencionando a API e o PriorityAdvisor).
- Stack Tecnológica.
- Arquitetura do Sistema (Explique brevemente a separação Controller/Services/Repository).
- Como Executar (Passo a passo com venv, pip install -e ".[dev]" e uvicorn na porta 8000).
- Suíte de Testes (Passo a passo para rodar pytest com banco em memória e mocks da IA).
- Roadmap de Releases (Tabela com Backend, Qualidade e Entrega Final).
- Fora de Escopo (Para alinhar expectativas de stakeholders).

Tom: Extremamente técnico, organizado e pragmático.
Público: Desenvolvedores, Engenheiros de QA e revisores técnicos de código.
Resposta: Crie o arquivo README.md com todo o conteúdo descrito. Sem comentários introdutórios.
Restrições: 
- SQLite: Reforce que não é necessário configurar PostgreSQL ou Docker. A camada Repository isola o banco de dados da lógica de negócio.
- Setup Realista: Inclua comandos de criação de venv, instalação (`pip install -e ".[dev]"`) e inicialização (`uvicorn main:app --reload`).
- Testes (Crucial): Especifique o uso de Dependency Overrides no FastAPI para rodar testes num SQLite em memória e o uso de mocks (`respx`) para isolar as chamadas externas.
- Escopo Negativo: Deixe explicitamente claro que o MVP **NÃO** contempla Frontend (GUI), infraestrutura em nuvem, Docker, bancos de dados externos ou sistemas de autenticação. O escopo negativo deve ser rigorosamente respeitado.
```

## Endpoint healtcheck

```
Atue como um Arquiteto de Software Sênior.
Contexto: O projeto é um MVP de Gerenciamento de Tarefas utilizando Python 3.12 e FastAPI, estruturado rigorosamente no padrão de arquitetura Controller-Service-Repository.
Objetivo: Crie o arquivo de inicialização app/main.py. Este arquivo deve instanciar a aplicação FastAPI (com metadados de título e versão) e expor um endpoint GET /health estruturado para monitoramento da API.
Estilo: Código limpo, estritamente aderente à PEP 8 e com tipagem explícita (strict type hinting). O código deve ser modular e documentado via docstrings Google.
Tom: Técnico, robusto e orientado a padrões de nível de produção.
Público: Desenvolvedores Backend e Engenheiros de QA que consumirão este arquivo como ponto de entrada da aplicação.
Resposta: Crie o arquivo app/main.py com o código Python. Não inclua textos introdutórios ou explicações externas ao código.
Tipagem da Resposta: Utilize o Pydantic para criar um modelo de dados (HealthCheckResponse) que garanta o contrato de saída do endpoint /health, retornando o status (string) e o timestamp (utilizando fuso horário UTC real).
```

## Modelagem de Dados

```
Atue como um Engenheiro Backend Sênior especialista em Python.
Contexto: Estamos na Release 1 do MVP de um Gerenciador de Tarefas construído com FastAPI. A arquitetura exige estrita separação entre a persistência (ORM) e validação de contratos (DTOs).
Objetivo: Criar os modelos e schemas essenciais para a entidade `Task`.
1. Em `app/models/task.py`: Crie o modelo do SQLAlchemy. Campos obrigatórios: id (PK, inteiro gerado pelo banco autoincrement), title (string, obrigatório), description (string, opcional), is_completed (booleano, default false), priority (string, default "Média").
2. Em `app/schemas/task.py`: Crie os schemas Pydantic: `TaskCreate` (entrada: apenas title e description, sem os campos de default como is_completed ou priority), `TaskUpdate` (entrada: permitir apenas a atualização do campo `is_completed` como opcional) e `TaskResponse` (saída: todos os campos, incluindo id).
Estilo: Código robusto, utilizando as extensões modernas do SQLAlchemy (Mapped e mapped_column) e do Pydantic (ConfigDict para model_config = {'from_attributes': True}).
Tom: Técnico e imperativo.
Público: Desenvolvedores da equipe de backend e o banco de dados local.
Resposta: Criei os arquivos com os códigos solicitados.
Restrições: Utilize apenas as bibliotecas nativas e a stack já estabelecida. O id não deve ser incluído nos schemas de Create e Update, apenas no Response.
```

## Acesso a Dados - Repository

```
Atue como um Especialista em Bancos de Dados e Desenvolvedor Python.
Contexto: Release 1 do MVP de Gerenciamento de Tarefas. Você deve implementar o padrão Repository para abstrair o acesso ao SQLite utilizando OBRIGATORIAMENTE o driver `aiosqlite` de forma completamente assíncrona.
Objetivo: Crie o arquivo `app/repositories/task_repository.py`. Este arquivo deve conter a classe `TaskRepository` que orquestra a sessão do banco (AsyncSession).
Implemente os seguintes métodos assíncronos:
- `create_task(task_data: TaskCreate, initial_priority: str = "Média") -> TaskResponse`
- `get_task(task_id: int) -> TaskResponse`
- `get_tasks(is_completed: bool = None, priority: str = None) -> list[TaskResponse]` (com construção dinâmica de query)
- `update_task(task_id: int, update_data: dict) -> TaskResponse`
- `update_task_priority(task_id: int, priority: str) -> None`
- `delete_task(task_id: int) -> bool`
Estilo: Aderente à PEP 8, com type hints estritos. O Repository deve receber a sessão (`AsyncSession`) no seu inicializador (Dependency Injection).
Tom: Pragmático e orientado à performance de concorrência local.
Público: O TaskService que consumirá esta classe, alheio aos detalhes de SQL.
Resposta: Crie o arquivo `app/repositories/task_repository.py` com o código Python.
Restrições: Para respeitar o RNF01, os métodos do repositório devem receber Pydantic e OBRIGATORIAMENTE retornar os schemas Pydantic (DTOs limpos). Nunca permita que instâncias ou objetos do SQLAlchemy "vazem" como retorno do Repository. Faça o mapping internamente de Entidade SQLAlchemy para `TaskResponse`. Lance `NoResultFound` ou devolva nulo para IDs não encontrados.
```

## PriorityAdvisor (IA Externa)

```
Atue como um Especialista em Integrações e Microsserviços baseados em IA.
Contexto: O backend FastAPI precisa consumir um serviço de IA (PriorityAdvisor) capaz de analisar o título e a descrição de uma tarefa para inferir a sua prioridade (Alta, Média ou Baixa). O sistema se conectará com uma API de LLM real (ex: OpenAI, Anthropic ou modelo local).
Objetivo: Crie o arquivo `app/services/priority_advisor.py` contendo a classe `PriorityAdvisorClient`.
O cliente deve ser instanciado via DI injetando o objeto `httpx.AsyncClient` e conter o método `suggest_priority(title: str, description: str) -> str`.
O cliente deve ser estruturado para consumir um endpoint de LLM. Você deve carregar a URL da API e a respectiva CHAVE DE API (API Key) a partir das variáveis de ambiente (`os.getenv`), nunca chumbando credenciais no código.
Crie um payload JSON robusto de prompt de sistema (System Prompt) instruindo o modelo a devolver estritamente uma única palavra ("Alta", "Média" ou "Baixa") como resposta.
O cliente deve ter um timeout rigoroso configurado (ex: 2 a 3 segundos) para evitar travamento da API local e prever blocos try/except para `httpx.RequestError` e `httpx.TimeoutException`.
Em caso de falha de conexão, timeout, erro de autenticação (401/403) ou se o modelo "alucinar" e não retornar uma das 3 palavras válidas, a função deve aplicar um "fallback silencioso", devolvendo imediatamente a prioridade padrão "Média".
Estilo: Código em Python moderno, assíncrono e muito defensivo contra indisponibilidade de rede e anomalias de LLMs. Utilize docstrings.
Tom: Profissional, robusto e focado em resiliência (fail-safe) e segurança de credenciais.
Público: O TaskService que usará esta classe.
Resposta: Criei o arquivo `app/services/priority_advisor.py` com o código Python.
Restrições: Cumpra as regras de injeção estrita do httpx, não faça hardcode de API Keys, lide defensivamente com a resposta em texto do LLM (limpando espaços/pontuação) e garanta o RNF05 de timeout/fallback.
```

## Service

```
Atue como um Engenheiro Backend especialista na camada de Lógica de Negócios (Business Logic).
Contexto: MVP de Gerenciador de Tarefas, Release 1. O Service é o coração da API. Ele precisa receber as chamadas dos endpoints e orquestrar as validações usando o Repositório e o Cliente de IA.
Objetivo: Crie o arquivo `app/services/task_services.py` com a classe `TaskService`.
O Service deve usar Injeção de Dependência (DI) em seu construtor para receber instâncias estritas de `TaskRepository` e `PriorityAdvisorClient`.
Implemente a lógica para delegar as funções CRUD ao Repositório.
Atenção Especial (RF02 e Background Tasks): Na função `create_task`, aplique a prioridade padrão ("Média") na chamada de criação no Repositório. Após a persistência, use a dependência `FastAPI BackgroundTasks` (recebida nos argumentos do endpoint e passada pro service) para engatilhar a chamada ao `PriorityAdvisorClient` assincronamente e, por conseguinte, solicitar ao repositório que atualize a tarefa caso a IA devolva uma prioridade nova (usando fallback silencioso e mantendo "Média" se a IA falhar).
Estilo: Python limpo. A camada de Service nunca vê as dependências HTTP do lado Web (Controller) nem strings SQL ou ORM (Repository).
Tom: Decisivo, centrado nas regras de negócios e orquestração.
Público: O controlador (Controller/Router) que consumirá o Service e instanciará a IA e o Repo via Depends do FastAPI.
Resposta: Crie o arquivo de código em `app/services/task_services.py` com a implementação do `TaskService`.
Restrições: Respeite os nomes das classes que você está importando (`TaskRepository` e `PriorityAdvisorClient`), garanta que o serviço utilize exclusivamente DTOs limpos do Pydantic (nunca objetos SQLAlchemy) e preveja o uso do `aiosqlite` no ecossistema global.
```

## Controller (Rotas da API)

```
Atue como um Especialista em FastAPI e Roteamento Web.
Contexto: MVP de Gerenciador de Tarefas, Release 1. Já possuímos a camada de Service (`TaskService`), Repository (`TaskRepository`) e Schemas Pydantic construídos.
Objetivo: Atualize o arquivo `app/main.py` (ou crie um `app/routers/tasks.py` e inclua no `main.py`). Adicione os endpoints REST na rota `/tasks` para as operações:
- `POST /tasks` (Criação)
- `GET /tasks` (Listagem com query parameters opcionais `is_completed` e `priority`)
- `GET /tasks/{task_id}` (Busca pontual)
- `PATCH /tasks/{task_id}` (Atualização estrita de `is_completed`)
- `DELETE /tasks/{task_id}` (Exclusão)
Estilo: Controladores EXTREMAMENTE finos. O Controller não deve conter regras de negócio, loops ou interações diretas com banco de dados. Ele deve apenas receber a requisição HTTP e injetar a dependência do Service via `Depends()` do FastAPI, repassando os DTOs.
Tom: Pragmático, focado no contrato REST.
Público: Consumidores da API (Frontend/QA).
Resposta: Faça as atualizações no arquivo `app/main.py` do Controller.
Restrições: Garanta a injeção do `TaskService` via `Depends()`. Utilize os códigos de status HTTP corretos no decorator da rota (ex: `status_code=201` para POST, `status_code=204` para DELETE). Ao instanciar as dependências para o Service, garanta o uso da sessão assíncrona (`AsyncSession`) no Repository.
````

# Testes Unitários, de Integração e Análise

## Testes da Camada de Service (Unitário)

```
Atue como um Desenvolvedor Backend Python Sênior e Especialista em Qualidade de Engenharia (QA)
Contexto: O CRUD do FastAPI está implementado em uma Clean Architecture. Precisamos testar isoladamente a camada de `Service`, que orquestra as regras de negócio e invoca o Repository e o PriorityAdvisor.
Objetivo: Crie o arquivo `app/tests/test_services.py` focado estritamente em testes unitários. Você deve utilizar `unittest.mock` (`MagicMock` ou `AsyncMock`, conforme aplicável) para "mockar" completamente as dependências do `Service` (ou seja, simule o retorno do `Repository` e do `PriorityAdvisor`). O objetivo é validar unicamente se o `Service` processa os dados corretamente e se levanta exceções (ex: `HTTPException` 404) quando o Repository não encontra o ID.
Estilo: Padrão AAA (Arrange, Act, Assert). Nomenclatura descritiva de testes (ex: `test_update_task_raises_404_when_id_not_found`).
Tom: Rigoroso e focado em testes de componentes isolados.
Público: Desenvolvedores e Engenheiros de Automação de Testes.
Resposta: Crie o arquivo app/tests/test_services.py com código Python. Não inclua textos explicativos antes ou depois do código.
Restrições: Não conecte ao banco de dados SQLite neste arquivo. Não force asserções para passarem artificialmente. O teste deve validar a implementação lógica real do Service. Se a lógica for falhar o teste, escreva o teste de forma coerente com o cenário de falha esperado. 
Mentalidade TDD (Red → Green): Não olhe para a implementação existente para escrever os testes, escreva-os baseados nos contratos e requisitos de negócio esperados. É desejável que os testes falhem (Red) caso a implementação atual do Service não cubra todos os cenários de erro e borda.
```

## Testes do PriorityAdvisor (Unitário / Comportamental)

```
Atue como um Desenvolvedor Backend Python Sênior e Especialista em Qualidade de Engenharia (QA).
Contexto:  Desenvolvemos o módulo `PriorityAdvisor`, uma função híbrida (assíncrona) que tenta consultar uma LLM via HTTP e possui um fallback seguro (heurística local por palavras-chave) caso a API externa falhe ou estoure o timeout.
Objetivo: Crie o arquivo `app/tests/test_priority_advisor.py`. Você deve garantir cobertura para três cenários críticos:
1. Sucesso: A chamada à LLM externa (mockada) retorna a prioridade.
2. Heurística Local: A requisição externa não possui chave ou é ignorada, e uma palavra-chave no título (ex: "urgente") força o retorno "Alta".
3. Timeout/Fallback: Simule um erro de `asyncio.TimeoutError` ou falha de rede na chamada externa e garanta que a função não levante erro, mas sim faça o fallback silencioso para a heurística local.

Estilo: Padrão AAA. Utilize explicitamente bibliotecas de mock HTTP modernas como `respx` ou `pytest-httpx` para interceptar as requisições assíncronas no nível de transporte, garantindo que o teste seja estritamente unitário.
Tom: Sistemático, validando resiliência e fail-safe.
Público: Engenheiros de Integração e QA.
Resposta: Crie o arquivo app/tests/test_priority_advisor.py com ódigo Python. Sem introduções textuais.
Restrições: A execução do Pytest deve ser instantânea. Nenhuma chamada de rede real deve ser feita. Valide estritamente se o bloco `try-except` da implementação do PriorityAdvisor está segurando o erro como desenhado.
**Mentalidade TDD (Red → Green):** Baseie as asserções de timeout e fallback estritamente no requisito de "falha segura" arquitetural. Se a implementação atual do `priority_advisor.py` não possuir um bloco `try-except` capturando `TimeoutError`, o teste **deve** ser escrito de forma que falhe (Red) ao rodar.
```

## Testes de Integração (API / Banco de Dados)

```
Atue como um Desenvolvedor Backend Python Sênior e Especialista em Qualidade de Engenharia (QA)
Contexto: Precisamos validar os contratos HTTP da nossa API FastAPI e a persistência real dos dados ponta-a-ponta, sem mockar o Service ou o Repository, caracterizando um teste de integração verdadeiro.
Objetivo: Desenvolva a suíte de testes de integração, composta por dois arquivos:
1. `app/tests/conftest.py`: Configure o `TestClient` da FastAPI. Crie a configuração (engine/session) para um banco SQLite temporário em memória (`sqlite:///:memory:`) e utilize o recurso `app.dependency_overrides` para injetar este banco de testes no lugar do banco de produção.
2. `app/tests/test_routers.py`: Consuma os endpoints via HTTP. Cubra fluxos de sucesso (criação 201, listagem 200, deleção 204) e trate de mapear erros de borda, especialmente `404 Not Found` e erros de validação Pydantic `422 Unprocessable Entity`. 

Estilo: Padrão AAA. Cada função de teste deve refletir uma requisição HTTP real e a asserção do JSON e do Status Code retornado.
Tom: Intolerante a falhas de contrato HTTP e persistência.
Público: Analistas de QA que manterão a esteira de CI/CD.
Resposta: Crie os arquivos app/tests/conftest.py e app/tests/test_routers.py com o código Python. Sem introduções textuais.
Restrições: O banco em memória deve ser criado (metadata.create_all) e destruído/limpo a cada execução de teste para garantir o isolamento. Não force o teste a dar PASS. Valide o comportamento HTTP real que o código atual fornece. Se a lógica for falhar o teste, escreva o teste de forma coerente com o cenário de falha esperado. Atenção à Arquitetura: Como o `TaskService` recebe a fábrica de conexões (`session_maker`) diretamente do escopo global em `main.py` para as Background Tasks, você **deve fazer o override da dependência `get_task_service` por completo** (injetando nela o repositório de teste e o `session_maker` de teste) para garantir que a rotina em background não vaze e não grave dados no banco de produção físico.
```

## Testes de Repositório (Integração com Banco de Dados)

```
Atue como um Desenvolvedor Backend Sênior e Especialista em Qualidade de Engenharia (QA)
Contexto: Arquitetura Python/FastAPI separa as responsabilidades em `models`, `repositories` e `services`. Precisamos testar exaustivamente a camada de acesso a dados, especificamente o arquivo `app/repositories/task_repository.py`. O objetivo é validar as queries do SQLAlchemy (inserções, atualizações e principalmente os filtros complexos) em um banco SQLite real, isolado da camada web (sem envolver o FastAPI).
Objetivo: Crie o arquivo `app/tests/test_task_repository.py`. Desenvolva testes que cubram as operações CRUD da entidade `Task` no banco de dados. 
Foque especialmente em testar a função de listagem (`get_tasks`), validando se os filtros opcionais de `is_completed` e `priority` (Alta, Média, Baixa) retornam os registros corretos quando combinados.
Estilo: Padrão rigoroso AAA (Arrange, Act, Assert). Nomenclatura descritiva e semântica (ex: `test_get_all_tasks_filters_by_high_priority_successfully`). O código deve ser modular, limpo e aderente à PEP 8.
Tom: Rigoroso, focado em integridade de dados e comportamento do ORM.
Público: Engenheiros de Dados e Analistas de Automação de QA.
Resposta: Criei o arquivo app/tests/test_task_repository.py com o código Python. Não inclua introduções ou explicações textuais.
Restrições: 
- **Sem Mocks de Banco:** Não utilize `MagicMock` ou `AsyncMock` para a sessão do banco. 
- **Fixture de Banco Real:** O arquivo deve criar ou importar uma *fixture* do `pytest` que instancie um banco SQLite em memória (`sqlite:///:memory:`) limpo para cada teste (criando as tabelas com `metadata.create_all` no *setup* e destruindo no *teardown*).
- **Inserção de Dados (Arrange):** Cada teste deve popular o banco de dados em memória com instâncias reais do modelo `Task` antes de executar a ação (Act) e asserção (Assert).
```