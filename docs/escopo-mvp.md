# Documento de Escopo - MVP Gerenciador de Tarefas

## 1. Objetivo Principal do MVP
Desenvolver uma Micro-API backend resiliente e testável para gerenciamento de tarefas (To-Do List). O sistema deve permitir o controle do ciclo de vida completo de uma tarefa e utilizar Inteligência Artificial (PriorityAdvisor) para sugerir automaticamente a prioridade de execução baseada no contexto da tarefa. O foco é entregar uma base arquitetural sólida (Controller-Service-Repository) em um prazo estrito de 30 horas.

## 2. Requisitos Funcionais (RF)
O sistema deve expor operações para a entidade `Task`.

| ID | Funcionalidade | Descrição e Comportamento Esperado |
| :--- | :--- | :--- |
| **RF01** | Criar Tarefa | O usuário deve poder criar uma tarefa fornecendo `title` (obrigatório) e `description` (opcional). |
| **RF02** | Sugestão de Prioridade (IA) | Durante a criação (RF01), o sistema deve atribuir uma prioridade padrão ("Média") e invocar o componente **PriorityAdvisor (AI)** em uma rotina de *background task* para atualizar o nível de prioridade assincronamente. Em caso de falha na IA, o sistema deve aplicar o *fallback* de forma silenciosa, mantendo a prioridade "Média" original. |
| **RF03** | Listar Tarefas | O sistema deve retornar uma lista de todas as tarefas cadastradas. |
| **RF04** | Filtrar Tarefas | A listagem (RF03) deve permitir filtros opcionais via *query parameters*: por **status de conclusão** (`is_completed`: booleano) e por **nível de prioridade** (`priority`: string). |
| **RF05** | Obter Tarefa Específica | O usuário deve poder buscar os detalhes de uma única tarefa através do seu identificador único (`task_id`). |
| **RF06** | Atualizar Tarefa | O usuário deve poder alterar parcialmente (PATCH) os dados de uma tarefa existente (ex: atualizar o título, alterar prioridade ou marcar como concluída/pendente). |
| **RF07** | Deletar Tarefa | O usuário deve poder remover permanentemente uma tarefa do sistema através do seu identificador. |

## 3. Requisitos Não Funcionais (RNF)

* **RNF01 - Arquitetura de Software:** O código deve aderir estritamente ao padrão **Controller-Service-Repository**, exigindo **Injeção de Dependência (DI)** explícita do Repositório e do Cliente HTTP (PriorityAdvisor) no construtor do Service. O Repositório deve entregar apenas **schemas Pydantic limpos (DTOs)** para o Service, garantindo que regras de negócio estejam isoladas das regras de acesso a banco de dados (evitando vazamento de entidades SQLAlchemy) e de roteamento web (Controller).
* **RNF02 - Persistência Local:** O armazenamento de dados deve ser feito em um banco de dados relacional local **SQLite** gerenciado através do ORM SQLAlchemy. Para prevenir travamentos (*database locks*) decorrentes da simultaneidade assíncrona, a aplicação deve utilizar obrigatoriamente o driver `aiosqlite` em conjunto com a extensão assíncrona do SQLAlchemy (`sqlalchemy.ext.asyncio`).
* **RNF03 - Tipagem e Validação:** A aplicação deve utilizar *type hints* rigorosos do Python 3.12+ e o Pydantic para validação de esquemas de entrada e saída (DTOs).
* **RNF04 - Testabilidade (QA):** O sistema deve ser desenhado para ter alta testabilidade. A automação de testes deve utilizar:
  * `pytest` como *test runner* principal.
  * `pytest-asyncio` para lidar com rotinas assíncronas (FastAPI e IA).
  * Sobrescrita de dependência (Dependency Overrides) para rodar testes integrados em um banco SQLite temporário em memória, utilizando obrigatoriamente `poolclass=StaticPool` no SQLAlchemy para evitar conflitos de escopo transacional.
  * O pacote `respx` associado ao `httpx` para isolar e "mockar" as requisições de rede externas feitas pelo PriorityAdvisor, garantindo que a suíte de testes nunca bata na rede real.
* **RNF05 - Resiliência de Integração:** O cliente HTTP (`httpx`) responsável por consumir o PriorityAdvisor (IA) deve implementar um *timeout* restrito (ex: 5 segundos) e garantir o tratamento (*catch*) de todas as exceções de rede para prevenir a degradação de desempenho da API.

## 4. Fora de Escopo (Out of Scope)
Para garantir o cumprimento do prazo de 30 horas, os seguintes itens estão explicitamente **excluídos** da entrega deste MVP:

* **Frontend/Interface Gráfica:** Não haverá desenvolvimento de telas web, painéis de admin ou aplicativos móveis.
* **Autenticação e Autorização:** Não haverá sistema de login, registro de usuários, emissão de tokens JWT ou controle de perfil de acessos (RBAC). A API será aberta.
* **Bancos de Dados Externos:** Migrações ou suporte configurado para PostgreSQL, MySQL ou infraestrutura de banco de dados em nuvem.
* **Deploy e DevOps:** Containerização complexa (Docker/Kubernetes), infraestrutura em nuvem (AWS/GCP/Azure) ou pipelines de CI/CD automatizados.
* **Notificações:** Envio de e-mails, SMS ou webhooks avisando sobre prazos de tarefas.
