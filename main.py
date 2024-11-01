import uvicorn
import jwt
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select
from db import get_session
from config import SUPABASE_SECRET_KEY, JWT_ALGORITHM

from models.products import Product
from models.categories import Category
from models.brands import Brand

BASE_URL = "http://localhost:8000"

app = FastAPI()

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:5173",
]

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SUPABASE_SECRET_KEY,
                             audience=["authenticated"],
                             algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/products')
async def get_products(session: Session = Depends(get_session)):
    statement = (
        select(Product, Category, Brand)
        .join(Category, Category.id == Product.category_id)
        .join(Brand, Brand.id == Product.brand_id)
    )
    results = session.exec(statement).all()

    products_list = [
        {
            "id": product.id,
            "brand": brand.name,
            "title": f"{brand.name} {product.title}",
            "image": f"{BASE_URL}/static/images/{product.image}",
            "description": product.description,
            "category": category.name,
            "price": product.price
        }
        for product, category, brand in results
    ]

    return products_list


@app.get('/products/{id}')
async def get_sing_product(id: int, session: Session = Depends(get_session)):
    statement = (
        select(Product, Category, Brand)
        .where(Product.id == id)
        .join(Category, Category.id == Product.category_id)
        .join(Brand, Brand.id == Product.brand_id)
    )
    result = session.exec(statement).first()

    product, category, brand = result

    product_details = {
        "id": product.id,
        "brand": brand.name,
        "title": f"{brand.name} {product.title}",
        "image": f"{BASE_URL}/static/images/{product.image}",
        "description": product.description,
        "category": category.name,
        "price": product.price
    }

    return product_details


@app.post('/products/add')
async def add_product(request: Product, credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())], session: Session = Depends(get_session)):
    if not credentials:
      raise HTTPException(status_code=403, detail="Not Authorized")

    token = credentials.credentials

    if not token:
      raise HTTPException(status_code=403, detail="Not Authorized")

    is_valid = verify_token(token)
    print(f"IS THE TOKEN VALID? {is_valid}, {token}")

    if not is_valid:
        raise HTTPException(status_code=403, detail="Not Authorized")

    session.add(request)
    session.commit()
    return {"message": request.title}


@app.get('/categories')
async def get_categories(session: Session = Depends(get_session)):
    statement = select(Category)
    results = session.exec(statement).all()
    categories = [
        category.name for category in results
    ]
    return categories


@app.get('/brands')
async def get_categories(session: Session = Depends(get_session)):
    statement = select(Brand)
    results = session.exec(statement).all()
    return results


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
