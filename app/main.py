from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import Base, engine, get_db
from . import schemas, models, crud


app = FastAPI(title="E‑commerce API (Supabase)")

@app.get("/")
def root():
    return {"message": "Welcome to the E-commerce API"}


Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Users ----
@app.post("/users", response_model=schemas.UserOut)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)


@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return


# ---- Sellers ----
@app.post("/sellers", response_model=schemas.SellerOut)
def create_seller(seller_in: schemas.SellerCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_seller(db, seller_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sellers", response_model=List[schemas.SellerOut])
def list_sellers(db: Session = Depends(get_db)):
    return crud.list_sellers(db)

# ---- Products (CRUD) ----
@app.post("/products", response_model=schemas.ProductOut, status_code=201)
def create_product(product_in: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product_in)

@app.get("/products", response_model=List[schemas.ProductOut])
def list_products(category: Optional[str] = Query(None, description="Filter by category"), db: Session = Depends(get_db)):
    return crud.list_products(db, category=category)

@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product_in: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = crud.update_product(db, product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return

@app.get("/categories", response_model=List[str])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)

@app.get("/products/by-category/{category}", response_model=List[schemas.ProductOut])
def list_products_by_category(category: str, db: Session = Depends(get_db)):
    return crud.list_products(db, category=category)

# ---- Orders ----
@app.post("/orders", response_model=schemas.OrderOut, status_code=201)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_order(db, order_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders", response_model=List[schemas.OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return crud.list_orders(db)

@app.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
