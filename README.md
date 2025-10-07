# API RESTful de Gestão de Ativos (Asset Management)

Esta aplicação é uma **API RESTful CRUD** para gerenciamento de **Usuários**, **Categorias** e **Dispositivos**. A arquitetura foi desenvolvida em **Python** utilizando **Flask**, com um foco central em segurança, validação de dados e facilidade de execução via Docker.

A API implementa todas as regras de negócio exigidas, como controle de unicidade de `serial`, bloqueio de exclusão de categoria com vínculos, e autenticação robusta via JWT.

---

## Tecnologias e Decisões Técnicas

| Categoria | Tecnologia | Decisão Técnica e Justificativa de Uso |
| :--- | :--- | :--- |
| **Backend** | Python, Flask | Escolha ideal para APIs de escopo médio/pequeno. Permite o **controle total** das bibliotecas e oferece alta velocidade de prototipagem e desenvolvimento. |
| **ORM/Database**| Flask-SQLAlchemy, SQLite | **SQLite** foi escolhido para simplificar o **setup inicial** e evitar dependências externas (como PostgreSQL ou MySQL) durante a execução via Docker Compose. |
| **Autenticação**| Flask-JWT-Extended | Padrão de segurança **stateless** (sem estado) robusto. Garante rotas protegidas com implementação mínima e alta eficiência. |
| **Validação** | Marshmallow | Essencial para garantir a **Validação de Entrada** em todos os *payloads* (`POST`/`PUT`/`PATCH`). Previne erros de tipagem e garante a integridade dos dados antes da lógica de negócio. |
| **Infraestrutura**| Docker, Docker Compose, Gunicorn | O **Docker Compose** garante a consistência do ambiente. **Gunicorn** é o servidor WSGI de produção padrão, oferecendo estabilidade e concorrência superior ao servidor de desenvolvimento do Flask. |
| **Versionamento BD** | Flask-Migrate (Alembic)| Crucial para o versionamento do *schema* do banco de dados, permitindo a **evolução segura** das tabelas sem perda de dados. |
| **Testes** | Pytest | Framework padrão, utilizado para cobrir as regras de negócio críticas (como bloqueio de exclusão e unicidade de serial), garantindo a estabilidade da aplicação. |

---

## Como Executar o Projeto

Recomendamos usar o Docker Compose para uma experiência consistente e rápida, pois ele gerencia todas as dependências e o servidor de produção (Gunicorn).

### Pré-requisitos

* Docker e Docker Compose
* (Opcional: Python 3.11+ e `pip` para execução local)

### Opção 1: Usando Docker Compose (Recomendado)

1.  **Configuração de Ambiente:** Crie o arquivo de ambiente e defina sua chave secreta (JWT_SECRET_KEY):
    ```bash
    cp .env.example .env
    # Edite o .env para uma chave JWT_SECRET_KEY forte.
    ```

2.  **Iniciar o Serviço:** O Docker Compose irá construir a imagem, aplicar as *migrations* (Flask-Migrate) e subir o Gunicorn.
    ```bash
    docker compose up --build
    ```

3.  A API estará acessível em `http://localhost:5000`.

### Opção 2: Execução Local (Python)

1.  **Setup:** Instale as dependências e defina a chave JWT:
    ```bash
    py -m venv venv
    .\venv\Scripts\activate  # Ativar o ambiente virtual no Windows
    py -m pip install -r requirements.txt
    set JWT_SECRET_KEY="SUA_CHAVE_FORTE"
    ```

2.  **Database:** Aplique as migrations para criar as tabelas:
    ```bash
    py -m flask db upgrade
    ```

3.  **Iniciar a Aplicação:**
    ```bash
    py -m flask run
    ```
    A API estará acessível em `http://127.0.0.1:5000`.

---

## Endpoints e Fluxo de Autenticação

Todos os endpoints de CRUD exigem o header `Authorization: Bearer <access_token>`.

### 1. Autenticação

| Rota | Método | Descrição |
| :--- | :--- | :--- |
| `/auth/register` | `POST` | Cria um novo usuário com senha *hashed*. |
| `/auth/login` | `POST` | Autentica o usuário e retorna o **JWT** necessário. |

**Exemplo de Login e Token (POST /auth/login)**
```json
{
  "username": "admin",
  "password": "123456"
}
// Resposta
{
  "access_token": "eyJhbGciOiJIUzI1NiI..." 
}
