from fastapi import FastAPI
from fastapi import APIRouter, Query
from typing import Annotated
from fastapi import Path

from task import task_router

app = FastAPI()

router = APIRouter()

@router.get('/')
def hello_world():
    return {"hello": "world"}

@app.get("/products/")
def get_products(
    category: str = Query(..., description="Categoría del producto", min_length=3, max_length=50),
    max_price: float = Query(100.0, gt=0, description="Precio máximo (opcional)")
):
    return {"category": category, "max_price": max_price}

@app.get("/e_page")
def page(page: int = Query(1, ge=1, le=20, title='Esta es la pagina que quieres ver'), size: int = Query(5, ge=5, le=20, title='Cuantos registros quieres ver')):
    return { "page": page, "size": size}

productos = [f"Producto {i}" for i in range(1, 101)]  # 100 productos

@app.get("/productos")
def listar_productos(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1)
):
    inicio = (page - 1) * size
    fin = inicio + size
    return productos[inicio:fin]

@app.get("/e_phone") # +34 111 12-34-56
def phone(
    phone: Annotated[
        str,
        Query(
            pattern=r"^\+?\d{1,3}\s?\d{3}\s?\d{2}[-\s]?\d{2}[-\s]?\d{2}$",
            description="Teléfono con formato +34 111 12-34-56"
        )
    ]
):
    return {"phone": phone}

@app.get("/phone2/")  #+34 111 12-34-56
def phone(phone: str = Query(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$")):
    return {"phone": phone}

@app.get("/products/")
def list_products(
    q: str = Query(
        default="",
        alias="search",
        title="Búsqueda",
        description="Texto para buscar productos",
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9\s]+$",
        deprecated=False,
        example="camiseta azul"
    ),
    page: int = Query(1, ge=1, le=100),
    limit: int = Query(10, ge=1, le=50)
):
    return {"search": q, "page": page, "limit": limit}

app.include_router(router)
app.include_router(task_router, prefix='/tasks')