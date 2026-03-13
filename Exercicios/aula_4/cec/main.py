from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    nome: str
    idade: int


# Envia a página HTML abaixo para o usuário
@app.get("/", response_class=HTMLResponse)
def render_html():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


# Adiciona um usuário numa lista
@app.post("/users", response_class=HTMLResponse)
def add_user(user: User):
    users.append(user.model_dump())
    return


# Lê todos os usuários da lista ou um índice específico (usando query parameter)
@app.get("/users", response_class=HTMLResponse)
def get_users(index: int | None = None):

    if len(users) == 0:
        return "<p>A lista está vazia.</p>"

    if index is not None:
        if index < 0 or index >= len(users):
            return f"<p>Não há usuário neste índice {index}</p>"
        u = users[index]
        return f"<p>{u['nome']}, {u['idade']}</p>"

    lista = ""
    for u in users:
        lista += f"{u["nome"]}, {u["idade"]} \n"

    return f"<pre>{lista}</pre>"


# Limpa a lista de usuários
@app.delete("/users", response_class=HTMLResponse)
def delete_all():
    users.clear()
    return "<p>Todos os usuários foram removidos.</p>"