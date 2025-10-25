from fastapi import FastAPI
from backend.database import init_db
from backend.routes import user_routes, product_routes, order_routes

app = FastAPI(
    title="Store Management API",
    version="1.0",
    description="API for managing users, products, categories, and orders."
)

# Initialize DB
init_db()

# Include routes
app.include_router(user_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Store Management API"}
