# TODO: Implement order endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Order, MenuItem
from app.schemas import OrderCreate, OrderOut
from app.database import get_db
from datetime import date


router = APIRouter()

LOG_FILE = "orders_log.txt"

@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    items = db.query(MenuItem).filter(MenuItem.id.in_(order.item_ids), MenuItem.is_available == True).all()
    if len(items) != len(order.item_ids):
        raise HTTPException(status_code=400, detail="Invalid or unavailable menu item(s).")

    total_price = sum(item.price for item in items)
    new_order = Order(customer_name=order.customer_name, items=items)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Logging
    log_line = f"{new_order.created_at.isoformat()} | {new_order.customer_name} | {[item.id for item in items]} | {total_price:.2f}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    return new_order

@router.get("/today/", response_model=list[OrderOut])
def get_today_orders(db: Session = Depends(get_db)):
    today = date.today()
    return db.query(Order).filter(func.date(Order.created_at) == today).all()