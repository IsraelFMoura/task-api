from fastapi import FastAPI

from core.database import Base, engine
from routers import auth, tasks

# Cria as tabelas no banco de dados (em produção, use Alembic para migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task API",
    description="API de gerenciamento de tarefas com autenticação JWT",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Task API no ar. Acesse /docs para a documentação interativa."}
