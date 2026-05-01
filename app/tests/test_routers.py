def test_create_task_success(client):
    # Arrange
    payload = {
        "title": "Tarefa de Teste API",
        "description": "Testando a integração completa",
    }

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Tarefa de Teste API"
    assert data["description"] == "Testando a integração completa"
    assert data["is_completed"] is False
    # No momento do retorno do POST a prioridade inicial é definida como 'Média'.
    # A background task modificará para 'Alta' posteriormente com o mock.
    assert data["priority"] == "Média"


def test_create_task_validation_error_invalid_priority_422(client):
    # Arrange: Tentando criar com uma prioridade fora do Literal permitido
    payload = {
        "title": "Tarefa com prioridade maliciosa",
        "priority": "Critica",  # O Schema Create nem permite prioridade, e se injetar, deve ser barrado/ignorado ou estourar no extra="forbid"
    }

    # Como no TaskCreate nós nem sequer declaramos o campo "priority", o Pydantic vai simplesmente ignorar.
    # Mas para ser estrito, se quisermos testar envio de tipos incorretos no POST, vamos testar o envio do 'title' como numérico
    payload_invalid_type = {
        "title": 12345,  # Título deve ser String
        "description": "Teste numérico",
    }

    # Act
    response = client.post("/tasks", json=payload_invalid_type)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["type"] == "string_type"
    # Arrange: Faltando o campo obrigatório 'title'
    payload = {"description": "O título é esquecido"}

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_list_tasks_success(client):
    # Arrange
    client.post("/tasks", json={"title": "Tarefa Alpha"})
    client.post("/tasks", json={"title": "Tarefa Beta"})

    # Act
    response = client.get("/tasks")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert type(data) is list
    assert len(data) >= 2


def test_get_task_by_id_success(client):
    # Arrange
    create_resp = client.post("/tasks", json={"title": "Tarefa Pontual"})
    task_id = create_resp.json()["id"]

    # Act
    response = client.get(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Tarefa Pontual"


def test_get_task_not_found_404(client):
    # Act
    response = client.get("/tasks/99999")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"


def test_update_task_success(client):
    # Arrange
    create_resp = client.post("/tasks", json={"title": "Tarefa Antes"})
    task_id = create_resp.json()["id"]

    update_payload = {
        "title": "Tarefa Depois",
        "is_completed": True,
        "priority": "Baixa",
    }

    # Act
    response = client.patch(f"/tasks/{task_id}", json=update_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Tarefa Depois"
    assert data["is_completed"] is True
    assert data["priority"] == "Baixa"


def test_update_task_not_found_404(client):
    # Act
    response = client.patch("/tasks/99999", json={"is_completed": True})

    # Assert
    assert response.status_code == 404


def test_delete_task_success(client):
    # Arrange
    create_resp = client.post("/tasks", json={"title": "Tarefa para Exclusão"})
    task_id = create_resp.json()["id"]

    # Act
    response = client.delete(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 204

    # Confirma que a exclusão foi persistida
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_delete_task_not_found_404(client):
    # Act
    response = client.delete("/tasks/99999")

    # Assert
    assert response.status_code == 404


def test_update_task_validation_error_invalid_priority_422(client):
    # Arrange
    create_resp = client.post("/tasks", json={"title": "Tarefa Prioridade Invalida"})
    task_id = create_resp.json()["id"]

    update_payload = {
        "priority": "Urgente"  # Inválido: apenas Alta, Média ou Baixa
    }

    # Act
    response = client.patch(f"/tasks/{task_id}", json=update_payload)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_create_task_validation_error_max_length_422(client):
    # Arrange: Título excedendo o limite de 100 caracteres
    payload = {"title": "A" * 101, "description": "Descrição normal"}

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["type"] == "string_too_long"


def test_create_task_validation_error_description_max_length_422(client):
    # Arrange: Descrição excedendo o limite de 500 caracteres
    payload = {"title": "Título normal", "description": "A" * 501}

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["type"] == "string_too_long"


def test_update_task_validation_error_invalid_boolean_422(client):
    # Arrange
    create_resp = client.post("/tasks", json={"title": "Tarefa Tipo Invalido"})
    task_id = create_resp.json()["id"]

    update_payload = {
        "is_completed": "isso_nao_e_booleano"  # Inválido: espera-se um booleano real
    }

    # Act
    response = client.patch(f"/tasks/{task_id}", json=update_payload)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["type"] == "bool_parsing"


def test_update_task_validation_error_max_length_422(client):
    # Arrange
    create_resp = client.post("/tasks", json={"title": "Tarefa Limite Titulo"})
    task_id = create_resp.json()["id"]

    update_payload = {"title": "A" * 101}

    # Act
    response = client.patch(f"/tasks/{task_id}", json=update_payload)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["type"] == "string_too_long"


def test_update_task_validation_error_description_max_length_422(client):
    # Arrange
    create_resp = client.post("/tasks", json={"title": "Tarefa Limite Descricao"})
    task_id = create_resp.json()["id"]

    update_payload = {"description": "B" * 501}

    # Act
    response = client.patch(f"/tasks/{task_id}", json=update_payload)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["type"] == "string_too_long"


def test_create_task_validation_error_null_title_422(client):
    # Arrange: Tentando criar com título explícito nulo (None/null no JSON)
    payload = {"title": None, "description": "Descrição válida"}

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["type"] == "string_type"


def test_create_task_success_null_description_201(client):
    # Arrange: Criando com descrição explicitamente nula
    payload = {"title": "Tarefa sem descrição", "description": None}

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Tarefa sem descrição"
    assert data["description"] is None


def test_update_task_success_null_description_200(client):
    # Arrange: Criação de uma tarefa com descrição
    create_payload = {
        "title": "Tarefa com descrição",
        "description": "Descrição original",
    }
    create_resp = client.post("/tasks", json=create_payload)
    task_id = create_resp.json()["id"]

    # Atualização enviando explicitamente null para a descrição
    update_payload = {"description": None}

    # Act
    response = client.patch(f"/tasks/{task_id}", json=update_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["description"] is None


def test_update_task_validation_error_null_title_422(client):
    # Arrange: Criação de uma tarefa normal
    create_resp = client.post(
        "/tasks", json={"title": "Tarefa Limite Titulo", "description": "foo"}
    )
    task_id = create_resp.json()["id"]

    # Tentando atualizar o título explicitamente para nulo (None/null no JSON)
    update_payload = {"title": None}

    # Act
    response = client.patch(f"/tasks/{task_id}", json=update_payload)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    # O Pydantic rejeita por conta do nosso field_validator customizado
    assert data["detail"][0]["type"] == "value_error"
