# API de Gerenciamento de Dispositivos

Esta aplicação fornece uma **API RESTful CRUD** robusta para a gestão de usuários, **Categorias** e **Dispositivos**. A API foi construída em **Python** utilizando o microframework **Flask**, com autenticação segura via **JWT (JSON Web Tokens)**.

O projeto cumpre integralmente todos os requisitos do desafio, com foco em boas práticas, validação de entrada rigorosa e infraestrutura simplificada via Docker.

---

## Decisões e Tecnologias Principais

| Categoria | Tecnologia | Justificativa de Uso (Decisões Técnicas) |
| :--- | :--- | :--- |
| **Backend** | Python, Flask | Escolha ideal para APIs pequenas/médias que exigem alta performance e controle, oferecendo flexibilidade e velocidade no desenvolvimento. |
| **ORM/Database**| Flask-SQLAlchemy, SQLite | SQLite foi escolhido para simplificar a execução em ambiente local/Docker, eliminando a necessidade de um banco de dados externo para o desafio. |
| **Autenticação**| Flask-JWT-Extended | Implementa um padrão de segurança **stateless** (sem estado) para rotas protegidas, garantindo acesso seguro com poucas linhas de código. |
| **Validação** | Marshmallow | Usado para garantir a **Validação de Entrada** de todos os payloads (`POST`/`PUT`/`PATCH`) de forma declarativa e padronizada, prevenindo erros e vulnerabilidades. |
| **Infraestrutura**| Docker, Docker Compose, Gunicorn | O **Docker Compose** garante a subida consistente do ambiente em qualquer SO. **Gunicorn** é o servidor WSGI de produção padrão para Python/Flask, oferecendo robustez e concorrência. |
| **Testes** | Pytest | Framework padrão e simples, usado para verificar as regras de negócio críticas (como bloqueio de exclusão e unicidade de serial). |
| **Migrations** | Flask-Migrate (Alembic) | Essencial para o versionamento e a evolução segura do schema do banco de dados (BDD), garantindo que as tabelas sejam criadas corretamente na inicialização. |

---

## Endpoints e Exemplos de Requisição

A coleção do **Postman** (`postman_collection.json`) já contém todos os endpoints configurados, mas os exemplos abaixo demonstram o fluxo principal da API.

**URL Base:** `http://localhost:5000`
**Header de Acesso (Necessário para todas as rotas de CRUD):** `Authorization: Bearer <access_token>`

### 1. Autenticação (POST)

| Rota | Request Body (JSON) | Response Body (JSON - Sucesso) |
| :--- | :--- | :--- |
| `/auth/register` | `{"username": "admin", "password": "123456"}` | `{"msg": "Usuário criado com sucesso"}` |
| `/auth/login` | `{"username": "admin", "password": "123456"}` | `{"access_token": "eyJhbGciOiJIUzI1NiI..."}` |

### 2. CRUD de Categorias

| Método | Rota | Descrição | Regras Específicas |
| :--- | :--- | :--- | :--- |
| `POST` | `/categorias` | Cria nova categoria. | `nome` é obrigatório e único. |
| `PUT/PATCH`| `/categorias/1` | Atualiza categoria. | Validação de `nome` único. |
| `DELETE` | `/categorias/1` | Exclui. | **Bloqueado (400)** se houver dispositivos vinculados. |

**Exemplo de Criação (POST /categorias)**
```json
{
  "nome": "Servidores",
  "descricao": "Máquinas de infraestrutura"
}
