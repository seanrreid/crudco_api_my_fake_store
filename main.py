import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from db import get_session

from models.products import Product
from models.categories import Category

app = FastAPI()

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:3000",
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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/products')
async def get_products(session: Session = Depends(get_session)):
    statement = select(Product, Category).join(
        Category, Category.id == Product.category_id)
    results = session.exec(statement).all()

    products_list = [
        {
            "id": product.id,
            "name": product.title,
            "image": product.image,
            "description": product.description,
            "category": category.name,
            "price": product.price
        }
        for product, category in results
    ]

    return products_list


@app.get('/categories')
async def get_categories(session: Session = Depends(get_session)):
    statement = select(Category)
    results = session.exec(statement).all()
    return results


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
