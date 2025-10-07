# API de Gerenciamento de Dispositivos

Esta aplicação fornece uma **API RESTful CRUD** para a gestão de usuários, **Categorias** e **Dispositivos**, construída em **Flask** e autenticada via **JWT**. O projeto cumpre todos os requisitos do desafio, com foco em boas práticas, segurança básica e facilidade de execução via Docker.

---

## Tecnologias Principais

| Categoria | Tecnologia | Justificativa de Uso (Decisões Técnicas) |
| :--- | :--- | :--- |
| **Backend** | Python, Flask | Escolha ideal para prototipagem rápida e APIs pequenas/médias, mantendo o controle total sobre as bibliotecas. |
| **ORM/Database**| Flask-SQLAlchemy, SQLite | SQLite foi escolhido para simplificar a execução em ambiente local/Docker, evitando dependências externas (como PostgreSQL) para o desafio. |
| **Autenticação**| Flask-JWT-Extended | Implementa um padrão de segurança robusto para rotas protegidas com poucas linhas de código. |
| **Validação** | Marshmallow | Usado para garantir a **Validação de Entrada** de todos os payloads (`POST`/`PUT`/`PATCH`), assegurando que os dados estejam limpos e completos antes de chegarem à lógica de negócio. |
| **Infraestrutura**| Docker, Docker Compose, Gunicorn | O Docker Compose garante a execução consistente em qualquer ambiente. Gunicorn é o servidor WSGI de produção padrão para Python/Flask, substituindo o servidor de desenvolvimento. |
| **Testes** | Pytest | Framework padrão para testes em Python, usado para verificar as regras de negócio críticas. |
| **Migrations** | Flask-Migrate (Alembic) | Essencial para o versionamento do banco de dados, permitindo a evolução segura do schema sem a perda de dados. |

---

## Como Executar o Projeto

### Pré-requisitos

* Docker e Docker Compose (Recomendado)
* Python e `pip` (Para execução local)

### Opção 1: Usando Docker Compose (Recomendado)

Esta é a maneira mais fácil de iniciar a API, pois ela constrói a imagem e aplica as migrations automaticamente.

1.  **Crie o arquivo de ambiente** a partir do template:
    ```bash
    cp .env.example .env
    # Edite o .env e defina uma JWT_SECRET_KEY forte.
    ```

2.  **Inicie o Serviço:** O Docker Compose irá aplicar as migrations e iniciar o Gunicorn na porta 5000.
    ```bash
    docker-compose up --build
    ```

3.  A API estará acessível em `http://localhost:5000`.

### Opção 2: Execução Local

1.  **Crie o arquivo de ambiente** (opcional, mas recomendado) e defina a chave JWT:
    ```bash
    # Exemplo: export JWT_SECRET_KEY="SUA_CHAVE_AQUI"
    ```

2.  **Crie o Virtual Environment e instale as dependências:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # ou venv\Scripts\activate no Windows
    pip install -r requirements.txt
    ```

3.  **Configuração do Flask-Migrate:**
    O projeto usa Migrations para criar e atualizar as tabelas.

    * **Executar a Migração Inicial:**
        ```bash
        flask db upgrade
        ```
        *(Isso criará o arquivo `app.db` e todas as tabelas.)*

4.  **Inicie a Aplicação:**
    ```bash
    flask run
    ```
    A API estará acessível em `http://127.0.0.1:5000`.

---

## Testes Automatizados

As regras de negócio críticas são cobertas por testes automatizados com Pytest.

**Para rodar os testes:**

```bash
# Certifique-se de estar no ambiente virtual ou no container
pytest
