from fastapi import FastAPI
import uvicorn

from mysite.api import users, products, orders, ai
from mysite.database.db import Base, engine
from mysite.admin.setup import setup_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Delivery Service')

app.include_router(users.user_router)
app.include_router(products.product_router)
app.include_router(orders.order_router)
app.include_router(ai.ai_router)

setup_admin(app)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)