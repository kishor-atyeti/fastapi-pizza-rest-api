from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id:Optional[int] = None
    username:str
    email:str
    password:str
    is_staff:Optional[bool] = False
    is_active:Optional[bool] = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'username': 'johndoe',
                'email': 'johndoe@example.com',
                'password': 'password',
                'is_staff': False,
                'is_active': True
            }
        }

class Settings(BaseModel):
    authjwt_secret_key:str = 'f6fcbb022001c77d7c9a41f724bbad7f9ae159535093ca5e99dc259d301e7fbb'

class LoginModel(BaseModel):
    username:str
    password:str

    class Config:
        json_schema_extra = {
            'example': {
                'username': 'johndoe',
                'password': 'password'
            }
        }

class OrderModel(BaseModel):
    id:Optional[int] = None
    quantity:int
    order_status:Optional[str] = 'PENDING'
    pizza_size:Optional[str] = 'SMALL'
    user_id:Optional[int] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'quantity': 2,
                'order_status': 'PENDING',
                'pizza_size': 'LARGE'
            }
        }


class SingleOrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    order_status: Optional[str] = 'PENDING'
    pizza_size: Optional[str] = 'SMALL'
    user_id: Optional[int] = None

