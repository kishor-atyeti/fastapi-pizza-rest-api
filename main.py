from fastapi import FastAPI, Security, Response
from auth_routes import auth_router
from order_routes import order_router
from schemas import Settings

# Global fastapi instance
app = FastAPI()

# Include the routers
app.include_router(auth_router)
app.include_router(order_router)

