from fastapi import FastAPI
from mysite.database.db import engine, Base
from mysite.api.users import user_router
from mysite.api.products import product_router
from mysite.api.orders import order_router
from mysite.admin.setup import setup_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Store API Orders")

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

setup_admin(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
