# Task API

API REST para gerenciamento de tarefas, com autenticação via JWT, construída com **FastAPI**.

Cada usuário se cadastra, faz login e gerencia apenas suas próprias tarefas — outros usuários não têm acesso a elas.

## ✨ Funcionalidades

- Cadastro e login de usuários (senhas criptografadas com `bcrypt`)
- Autenticação via **JWT** (Bearer Token)
- CRUD completo de tarefas (criar, listar, buscar, atualizar, deletar)
- Isolamento de dados: cada usuário só vê suas próprias tarefas
- Filtro de tarefas por status (concluída/pendente)
- Documentação interativa automática (Swagger e ReDoc)
- Testes automatizados com `pytest`

## 🛠️ Stack

- **Python 3.12**
- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **SQLite** — banco de dados (fácil de rodar localmente, sem setup extra)
- **python-jose** — geração e validação de tokens JWT
- **bcrypt** — hash de senhas
- **pytest** — testes automatizados

## 📁 Estrutura do projeto

```
task-api/
├── main.py                 # Ponto de entrada da aplicação
├── core/
│   ├── database.py         # Configuração do banco de dados
│   ├── security.py         # Hash de senha e geração/validação de JWT
│   └── deps.py              # Dependências (ex: usuário autenticado atual)
├── models/
│   └── models.py            # Modelos SQLAlchemy (User, Task)
├── schemas/
│   └── schemas.py            # Schemas Pydantic (validação de entrada/saída)
├── routers/
│   ├── auth.py               # Rotas de registro e login
│   └── tasks.py               # Rotas de CRUD de tarefas
├── tests/
│   └── test_api.py            # Testes automatizados
├── requirements.txt
└── .env.example
```

## 🚀 Como rodar localmente

### 1. Clone o repositório e entre na pasta

```bash
git clone <url-do-seu-repositorio>
cd task-api
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente (opcional)

```bash
cp .env.example .env
# edite o .env e defina uma SECRET_KEY própria
```

### 5. Rode o servidor

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.

### 6. Acesse a documentação interativa

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Rodando os testes

```bash
pytest tests/ -v
```

## 📖 Exemplos de uso

### Cadastrar um usuário

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@example.com", "password": "senha123"}'
```

### Fazer login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@example.com&password=senha123"
```

A resposta traz um `access_token` — use-o no header `Authorization: Bearer <token>` nas próximas requisições.

### Criar uma tarefa

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <seu-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar FastAPI", "description": "Terminar o projeto de portfólio"}'
```

### Listar tarefas

```bash
curl http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <seu-token>"
```

## 🔒 Sobre segurança

Este é um projeto de portfólio/estudo. Antes de usar em produção, considere:

- Usar HTTPS
- Definir uma `SECRET_KEY` forte e única via variável de ambiente
- Migrar de SQLite para PostgreSQL
- Adicionar rate limiting nas rotas de login
- Implementar refresh tokens

## 📝 Licença

Este projeto está sob a licença MIT — sinta-se livre para usá-lo como referência.
