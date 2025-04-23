from fastapi import APIRouter, status, Depends, Response, Security
from database import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt import JwtAccessBearer, JwtRefreshCookie, JwtAuthorizationCredentials

# APIRouter instance for authentication
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session = Session(bind=engine)

access_security = JwtAccessBearer(
    secret_key='f6fcbb022001c77d7c9a41f724bbad7f9ae159535093ca5e99dc259d301e7fbb',
    auto_error=True
)

@auth_router.get('/')
async def hello():
    return {
        "message": "Hello World"
    }

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    db_username = session.query(User).filter(User.username==user.username).first()
    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )

    session.add(new_user)
    session.commit()

    return True

@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel, response: Response):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        subject = {
            "username": db_user.username,
            "email": db_user.email
        }
        access_token = access_security.create_access_token(subject=subject)
        refresh_token = access_security.create_refresh_token(subject=subject)
        access_security.set_access_cookie(response, access_token)

        tokens = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(tokens)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid username or password"
    )

@auth_router.get("/users/me")
def read_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    try:
        return {"username": credentials["username"], "email": credentials["email"]}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )