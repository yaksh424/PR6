from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Dict

app = FastAPI(title="Шаблоны в FastAPI — ПЗ№6")

# Статика и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Простейшее in-memory хранилище (для демонстрации шаблонов)
_items: List[Dict] = [
    {"id": 1, "title": "Пример записи 1", "description": "Короткое описание для записи 1."},
    {"id": 2, "title": "Пример записи 2", "description": "Короткое описание для записи 2."},
]
_next_id = 3


@app.get("/", include_in_schema=True)
async def index(request: Request):
    """Список записей — демонстрация цикла, условных блоков и наследования шаблонов."""
    return templates.TemplateResponse("index.html", {"request": request, "items": _items})


@app.get("/item/{item_id}")
async def item_detail(request: Request, item_id: int):
    """Страница с детальной информацией о записи."""
    item = next((i for i in _items if i["id"] == item_id), None)
    if item is None:
        return templates.TemplateResponse("detail.html", {"request": request, "item": None, "not_found": True})
    return templates.TemplateResponse("detail.html", {"request": request, "item": item, "not_found": False})


@app.get("/create")
async def create_form(request: Request):
    """Форма для создания новой записи (GET)."""
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/create")
async def create_post(request: Request, title: str = Form(...), description: str = Form("")):
    """Обработка POST-запроса формы создания записи."""
    global _next_id
    item = {"id": _next_id, "title": title, "description": description}
    _items.append(item)
    _next_id += 1
    # Редирект на главную страницу (POST -> Redirect)
    return RedirectResponse(url='/', status_code=303)


# Небольшой хелпер-роут для демонстрации макросов/включений (необязательно)
@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
