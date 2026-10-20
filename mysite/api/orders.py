from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import get_db
from mysite.database.models import Order, User, Product
from mysite.database.schema import OrderCreate, OrderResponse

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь и продукт
    user = db.query(User).filter(User.id == order.user_id).first()
    product = db.query(Product).filter(Product.id == order.product_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    new_order = Order(**order.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@order_router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()