from fastapi import APIRouter, Security, status
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from models import User, Order
from schemas import OrderModel, SingleOrderModel
from database import engine, Session
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

session = Session(bind=engine)

access_security = JwtAccessBearer(secret_key='f6fcbb022001c77d7c9a41f724bbad7f9ae159535093ca5e99dc259d301e7fbb', auto_error=True)

# APIRouter instance for orders
order_router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@order_router.get('/hello_world')
async def hello_world(
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    return {
        "message": "Hello World2"
    }

@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(
        order: OrderModel,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    current_user_username = credentials["username"]
    user = session.query(User).filter(User.username==current_user_username).first()

    new_order = Order(
        pizza_size= order.pizza_size,
        quantity=order.quantity
    )
    new_order.user = user
    session.add(new_order)
    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)

@order_router.get('/orders', status_code=status.HTTP_200_OK)
async def get_all_orders(
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    stmt = session.query(Order).all()



    # response = {
    #     "status": True,
    #     "message": "All orders fetched",
    #     "data": orders
    # }

    return jsonable_encoder(stmt)