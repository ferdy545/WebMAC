from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import Aluno
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

def buscar_alunos(busca):
    with Session(engine) as session:
        query = select(Aluno).where(Aluno.nome.ilike(f"%{busca}%")).order_by(Aluno.nome)
        return session.exec(query).all()


@asynccontextmanager
async def initFunction(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=initFunction)
app.mount("/Static", StaticFiles(directory="static"), name="static")

arquivo_sqlite = "HTMX2.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"
engine = create_engine(url_sqlite)

templates = Jinja2Templates(directory=["Templates", "Templates/Partials"])


@app.get("/busca", response_class=HTMLResponse)
def busca(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/lista", response_class=HTMLResponse)
def lista(request: Request, busca: str | None = '', pagina: int = 1, limite: int = 10):
    
    lista_alunos = buscar_alunos(busca)
    tamanho_lista = len(lista_alunos)
    i = (pagina - 1) * limite
    j = i + limite
    alunos = lista_alunos[i:j]
    comeco_lista = pagina <= 1
    final_lista = j >= tamanho_lista

    return templates.TemplateResponse(request, "lista.html",
        {
            "alunos": alunos,
            "pagina": pagina,
            "limite": limite,
            "busca": busca,
            "comeco_lista": comeco_lista,
            "final_lista": final_lista
        }
    )


@app.get("/editarAlunos")
def novoAluno(request: Request):
    return templates.TemplateResponse(request, "options.html")


@app.post("/novoAluno", response_class=HTMLResponse)
def criar_aluno(nome: str = Form(...)):
    with Session(engine) as session:
        novo_aluno = Aluno(nome=nome)
        session.add(novo_aluno)
        session.commit()
        session.refresh(novo_aluno)
        return HTMLResponse(content=f"<p>O(a) aluno(a) {novo_aluno.nome} foi registrado(a)!</p>")


@app.put("/atualizaAluno", response_class=HTMLResponse)
def atualizar_aluno(id: int = Form(...), novoNome: str = Form(...)):
    with Session(engine) as session:
        query = select(Aluno).where(Aluno.id == id)
        aluno = session.exec(query).first()
        if (not aluno):
            raise HTTPException(404, "Aluno não encontrado")
        nomeAntigo = aluno.nome
        aluno.nome = novoNome
        session.commit()
        session.refresh(aluno)
        return HTMLResponse(content=f"<p>O(a) aluno(a) {nomeAntigo} foi atualizado(a) para {aluno.nome}!</p>")
    

@app.delete("/deletaAluno", response_class=HTMLResponse)
def deletar_aluno(id: int = Form(...)):
    with Session(engine) as session:
        query = select(Aluno).where(Aluno.id == id)
        aluno = session.exec(query).first()
        if (not aluno):
            raise HTTPException(404, "Aluno não encontrado")
        session.delete(aluno)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) aluno(a) {aluno.nome} foi deletado(a)!</p>")


@app.delete("/apagar", response_class=HTMLResponse)
def apagar():
    return ""