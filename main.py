import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from db import get_session

from models.products import Product
from models.categories import Category
from models.brands import Brand

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
    statement = (
        select(Product, Category, Brand)
        .join(Category, Category.id == Product.category_id)
        .join(Brand, Brand.id == Product.brand_id)
    )
    results = session.exec(statement).all()
    print(results)

    products_list = [
        {
            "id": product.id,
            "brand": brand.name,
            "name": product.title,
            "image": product.image,
            "description": product.description,
            "category": category.name,
            "price": product.price
        }
        for product, category, brand in results
    ]

    return products_list


@app.get('/categories')
async def get_categories(session: Session = Depends(get_session)):
    statement = select(Category)
    results = session.exec(statement).all()
    return results


@app.get('/brands')
async def get_categories(session: Session = Depends(get_session)):
    statement = select(Brand)
    results = session.exec(statement).all()
    return results


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
