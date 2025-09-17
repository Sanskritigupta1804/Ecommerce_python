from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from . import models, schemas
from passlib.hash import bcrypt

# ---- Users ----
def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    user = models.User(
        email=user_in.email, full_name=user_in.full_name, hashed_password=bcrypt.hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session) -> List[models.User]:
    return db.scalars(select(models.User)).all()

def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate) -> Optional[models.User]:
    """Update user fields"""
    user = db.get(models.User, user_id)
    if not user:
        return None

    data = user_in.model_dump(exclude_unset=True)
    if "password" in data:
        data["hashed_password"] = bcrypt.hash(data.pop("password"))

    for k, v in data.items():
        setattr(user, k, v)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    user = db.get(models.User, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

# ---- Sellers ----
def create_seller(db: Session, seller_in: schemas.SellerCreate) -> models.Seller:
    seller = models.Seller(name=seller_in.name, email=seller_in.email)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller

def list_sellers(db: Session) -> List[models.Seller]:
    return db.scalars(select(models.Seller)).all()

# ---- Products (CRUD) ----
def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    product = models.Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.get(models.Product, product_id)

def list_products(db: Session, category: Optional[str] = None) -> List[models.Product]:
    stmt = select(models.Product)
    if category:
        stmt = stmt.where(models.Product.category == category)
    return db.scalars(stmt).all()

def update_product(db: Session, product_id: int, product_in: schemas.ProductUpdate) -> Optional[models.Product]:
    product = db.get(models.Product, product_id)
    if not product:
        return None
    data = product_in.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(product, k, v)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> bool:
    product = db.get(models.Product, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True

def list_categories(db: Session) -> List[str]:
    rows = db.execute(select(func.distinct(models.Product.category))).all()
    return [row[0] for row in rows]

# ---- Orders ----
def create_order(db: Session, order_in: schemas.OrderCreate) -> models.Order:
    user = db.get(models.User, order_in.user_id)
    if not user:
        raise ValueError("User not found")

    order = models.Order(user_id=order_in.user_id, status="PENDING")
    db.add(order)
    db.flush()  # get order.id

    total = 0.0
    for item in order_in.items:
        product = db.get(models.Product, item.product_id)
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for product {product.id}")

        # reduce stock
        product.stock -= item.quantity

        unit_price = float(product.price)
        total += unit_price * item.quantity

        db.add(models.OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, unit_price=unit_price))

    order.total_amount = total
    order.status = "CONFIRMED"
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    return db.get(models.Order, order_id)

def list_orders(db: Session) -> List[models.Order]:
    return db.scalars(select(models.Order)).all()
