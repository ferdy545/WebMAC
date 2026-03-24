from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="./")

contador = 0


def render_page(request: Request, aba: str, context: dict | None = None):
    if context is None:
        context = {}

    context["contador"] = contador

    if "HX-Request" in request.headers:
        return templates.TemplateResponse(request=request, name=aba, context=context)

    return templates.TemplateResponse(request=request,name="index.html", context={"pagina": request.url.path})


@app.post("/curtir", response_class=HTMLResponse)
async def curtir(request: Request):
    global contador
    contador += 1
    return render_page(request, "curtir.html", {"contador": contador})


@app.post("/zerar", response_class=HTMLResponse)
async def zerar(request: Request):
    global contador
    contador = 0
    return render_page(request, "curtir.html", {"contador": contador})


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    global contador
    return render_page(request, "curtir.html", {"contador": contador})


@app.get("/home/jupiter", response_class=HTMLResponse)
async def jupiter(request: Request):
    return render_page(request, "jupiter.html")


@app.get("/home/professor", response_class=HTMLResponse)
async def professor(request: Request):
    return render_page(request, "professor.html")