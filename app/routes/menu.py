from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from app import models, schemas
from app.database import get_db
import os

router = APIRouter()

@router.post("/", response_model=schemas.MenuItemOut)
def create_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    db_item = models.MenuItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/available/", response_model=list[schemas.MenuItemOut])
def get_available_menu_items(db: Session = Depends(get_db)):
    return db.query(models.MenuItem).filter(models.MenuItem.is_available == True).all()

@router.post("/order/", response_model=schemas.OrderOut)
def place_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    items = db.query(models.MenuItem).filter(models.MenuItem.id.in_(order.item_ids)).all()
    if len(items) != len(order.item_ids):
        raise HTTPException(status_code=400, detail="Some menu items not found")

    unavailable = [item.id for item in items if not item.is_available]
    if unavailable:
        raise HTTPException(status_code=400, detail=f"Items not available: {unavailable}")

    db_order = models.Order(customer_name=order.customer_name, items=items)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    total_price = sum(item.price for item in items)
    timestamp = db_order.created_at.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} | {order.customer_name} | {order.item_ids} | {total_price:.2f}\n"
    with open("orders_log.txt", "a") as f:
        f.write(log_line)

    return db_order

@router.get("/orders/today/", response_model=list[schemas.OrderOut])
def get_todays_orders(db: Session = Depends(get_db)):
    today = date.today()
    return db.query(models.Order).filter(models.Order.created_at >= datetime.combine(today, datetime.min.time())).all()
