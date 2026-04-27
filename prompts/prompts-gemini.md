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