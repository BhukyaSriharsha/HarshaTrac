from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://harsha-trac.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hello, World!"

products = [
    Product(id=1, name="phone", description="smartphone", price=699.99, quantity=50),
    Product(id=2, name="laptop", description="gaming laptop", price=1299.99, quantity=30),
    Product(id=3, name="headphones", description="wireless headphones", price=199.99, quantity=100),
]


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

def init_db():
    db = SessionLocal()

    count = db.query(database_models.Product).count 
    if(count == 0):
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
    
    db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    #db = SessionLocal()
    #db.query()

    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product Not found"
    
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)): 
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, update_product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = update_product.name
        db_product.description = update_product.description
        db_product.price = update_product.price
        db_product.quantity = update_product.quantity
        db.commit()
        return "Product Updated Successfully"
    else:    
        return "Product Not found"   
        
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted Successfully"
    else: 
        return "Product Not found"