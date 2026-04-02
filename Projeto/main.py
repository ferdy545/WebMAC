from database import create_db, get_session
from models import Bagulho, Categoria

from fastapi import FastAPI, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

import random

# =================================================================================================

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

create_db()

debate_serio = []

# =================================================================================================

# Página A (index.html)
@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse("static/index.html")

# =================================================================================================

# Página B (manage.html)
@app.get("/manage", response_class=HTMLResponse)
def manage():
    return FileResponse("static/manage.html")

# =================================================================================================

# Critério de atualização de pontos com base na escolha feita
def ranking_algorithm(winner: Bagulho, loser: Bagulho):

    expected_winner = 1 / (1 + 10 ** ((loser.score - winner.score) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner.score - loser.score) / 400))
    
    winner.score += round(16 * (1 - expected_winner))
    loser.score += round(16 * (0 - expected_loser))

# =================================================================================================

# Mostrar dois Bagulhos aleatoriamente em index.html
@app.get("/choice", response_class=HTMLResponse)
def get_choice(request: Request, session: Session = Depends(get_session)):

    global debate_serio

    lista_bagulhos = session.exec(select(Bagulho)).all()

    if len(lista_bagulhos) < 2:
        return HTMLResponse('<p style="width: fit-content; margin: 0 auto;">É necessário haver ao menos dois Bagulhos registrados!</p>')

    if not debate_serio or not all(session.get(Bagulho, id) for id in debate_serio):
        bagulho1, bagulho2 = random.sample(lista_bagulhos, 2)
        debate_serio = [bagulho1.id, bagulho2.id]
    else:
        bagulho1 = session.get(Bagulho, debate_serio[0])
        bagulho2 = session.get(Bagulho, debate_serio[1])

    return templates.TemplateResponse(
        request = request,
        name = "choice.html", 
        context = {"bagulho1": bagulho1, "bagulho2": bagulho2}
    )

# =================================================================================================

# Atualizar o score depois de clicar no botão em uma das cartas e depois mostrar dois Bagulhos novamente
@app.post("/update_score/{winner_id}/{loser_id}")
def update_score(winner_id: int, loser_id: int, request: Request, session: Session = Depends(get_session)):

    global debate_serio

    winner = session.get(Bagulho, winner_id)
    loser = session.get(Bagulho, loser_id)

    if winner and loser:
        ranking_algorithm(winner, loser)
        session.add(winner)
        session.add(loser)
        session.commit()

    debate_serio.clear() 
    
    return get_choice(request, session)

# =================================================================================================

# Excluir Bagulho ao clicar no botão de lixeira em algum card na tela B (manage.html)
@app.delete("/excluir_bagulho/{id}")
def delete_bagulho(id: int, session: Session = Depends(get_session)):

    bagulho = session.get(Bagulho, id)

    if not bagulho:
        return {"error": "Not found"}

    categoria_id = bagulho.categoria_id

    session.delete(bagulho)
    session.commit()

    # listar todos os Bagulhos que estão na mesma Categoria do bauglho que acabou de ser excluído
    lista_bagulhos = session.exec(select(Bagulho).where(Bagulho.categoria_id == categoria_id)).first()

    # se não tiver nenhum Bagulho, a categoria está vazia, então exclui a Categoria também
    if not lista_bagulhos:
        category = session.get(Categoria, categoria_id)
        session.delete(category)
        session.commit()

    return Response(headers={"HX-Trigger": "reloadList"})

# =================================================================================================

# Listar Bagulhos em order descrescente de score, em 'paginação infinita'
@app.get("/listar_bagulhos", response_class=HTMLResponse)
def list_bagulhos(request: Request,
                  offset: int = 0,
                  limit: int = 10,
                  session: Session = Depends(get_session)):
    
    # neste caso vamos sempre mostrando de 10 em 10 (limit)
    results = session.exec(
        select(Bagulho)
        .order_by(Bagulho.score.desc())
        .offset(offset)
        .limit(limit + 1)
    ).all()

    has_more = len(results) > limit
    bagulhos = results[:limit]

    return templates.TemplateResponse(
        request=request,
        name="card_list.html",
        context={
            "bagulhos": bagulhos,
            "next_offset": offset + limit,
            "limit": limit,
            "has_more": has_more,
            "position_start": offset + 1
        }
    )

# =================================================================================================

# Criar um Bagulho novo ao clicar no botão 'Adicionar' em manage.html
@app.post("/criar_bagulho", response_class=HTMLResponse)
def create_bagulho(nome: str = Form(...),
                   categoria: str = Form(...),
                   imagem: str = Form(""),
                   session: Session = Depends(get_session)):


    nome = nome.upper()
    categoria = categoria.lower()

    # seleciona a Categoria do Bagulho criado, se ela já existir no banco de dados
    new_category = session.exec(select(Categoria).where(Categoria.nome == categoria)).first()

    # se não existir a Categoria do Bagulho criado, então cria uma nova Categoria
    if not new_category:
        new_category = Categoria(nome=categoria)
        session.add(new_category)
        session.commit()
        session.refresh(new_category)

    bagulho = Bagulho(
        nome=nome,
        imagem=imagem if imagem else "/static/placeholder.png",
        categoria_id=new_category.id
    )

    try:
        session.add(bagulho)
        session.commit()
        return Response(headers={"HX-Trigger": "reloadList"})
    
    except IntegrityError:
        session.rollback()
        return HTMLResponse('<p style="color: rgb(255, 0, 0); margin-top: 5px;">Esse Bagulho já existe!</p>')