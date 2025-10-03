# 📡 API de Gerenciamento de Dispositivos

Esta aplicação fornece uma API RESTful para **gestão de usuários, categorias e dispositivos**, construída em **Flask** com suporte a autenticação baseada em **JWT (JSON Web Tokens)**.  

O projeto segue boas práticas de arquitetura, utilizando **SQLAlchemy** como ORM, **Flask-Migrate** para versionamento de banco de dados, e **pytest** para testes automatizados.  
Entre as regras de negócio críticas implementadas destacam-se:  

- Bloqueio da exclusão de categorias que possuam dispositivos vinculados.  
- Validação de seriais únicos para dispositivos.  
- Controle de status de dispositivos (`ativo` / `inativo`).  

---

## 🛠️ Tecnologias

**Linguagens:**  
- Python  
- SQL (SQLite)  
- JSON (padrão de comunicação)  

**Frameworks e bibliotecas:**  
- [Flask](https://flask.palletsprojects.com/) – microframework web  
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) – ORM  
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) – migrações (Alembic)  
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) – autenticação JWT  
- [Werkzeug](https://werkzeug.palletsprojects.com/) – utilitário de segurança (hash de senhas)  
- [Pytest](https://docs.pytest.org/) – framework de testes  
- [Gunicorn](https://gunicorn.org/) – servidor WSGI de produção  

**Banco de dados:**  
- SQLite (padrão, pode ser substituído por outros compatíveis com SQLAlchemy)  

**Protocolo:**  
- HTTP (RESTful)  

---

## 📂 Estrutura do Projeto
