.PHONY: help run test clean-db seed reset-db install lint format

# Target padrão executado ao chamar apenas `make`
.DEFAULT_GOAL := help

# Lista todos os comandos disponíveis
help:
	@echo "Comandos disponiveis:"
	@echo "  make run        - Executa a aplicacao FastAPI com recarregamento automatico"
	@echo "  make test       - Executa toda a suite de testes"
	@echo "  make install    - Instala as dependencias do projeto"
	@echo "  make clean-db   - Apaga o banco de dados local SQLite"
	@echo "  make seed       - Roda o script para recriar as tabelas e popular o banco de dados"
	@echo "  make reset-db   - Fluxo completo: apaga o banco atual e repopula do zero"
	@echo "  make lint       - Executa checagem de estilo de codigo e de tipos estaticos"
	@echo "  make format     - Formata o codigo automaticamente e corrige erros de estilo"
	@echo ""

# Variáveis
DB_FILE = tasks.db
PYTHON = python
UVICORN = uvicorn
PYTEST = pytest
RUFF = ruff
MYPY = mypy

# Executa a aplicação FastAPI com recarregamento automático
run:
	$(UVICORN) app.main:app --reload --port 8000

# Executa toda a suíte de testes
test:
	$(PYTEST) -v

# Executa o linting e checagem de tipos
lint:
	@echo "Executando linting com Ruff..."
	$(RUFF) check .
	@echo "Verificando tipos com Mypy..."
	$(MYPY) app

# Formata o código automaticamente e corrige erros de estilo
format:
	@echo "Formatando o código com Ruff..."
	$(RUFF) format .
	$(RUFF) check --fix .

# Instala as dependências do projeto
install:
	$(PYTHON) -m pip install -r requirements.txt

# Apaga o banco de dados local SQLite
clean-db:
	@echo "Removendo banco de dados $(DB_FILE)..."
	-rm -f $(DB_FILE)
	-del /Q /F $(DB_FILE) 2>nul || true

# Roda o script para recriar as tabelas e popular o banco de dados
seed:
	@echo "Populando banco de dados..."
	$(PYTHON) seed_db.py

# Fluxo completo: apaga o banco atual e repopula do zero
reset-db: clean-db seed
	@echo "Banco de dados resetado com sucesso!"
