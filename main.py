from fastapi import FastAPI, Request
from time import time
from app.routes import menu, order
from app.database import engine
from app.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def log_request_data(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    duration = time() - start_time
    print(f"{request.method} {request.url.path} completed in {duration:.4f}s")
    return response

app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(order.router, prefix="/order", tags=["Order"])