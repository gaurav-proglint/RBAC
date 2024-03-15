from fastapi import FastAPI, Depends, HTTPException, status,Request,Body
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
import jwt
from datetime import datetime,timedelta,timezone
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import models
import json
from middlewares import FieldValidationMiddleware
from database import engine
#from starlette.requests import FormData
from starlette.datastructures import FormData
import io
from crud import get_user,insert_token
from database import get_db
from pydantic import BaseModel
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# @app.middleware("http")
# async def custom_middleware(request: Request, call_next):
#     print(request)
#     try:
#         if request.url.path == "/login" and request.method == 'POST':
#             await FieldValidationMiddleware.validate_input_login(request)
           
#     except HTTPException as exc:
#         return JSONResponse({"error": exc.detail}, status_code=exc.status_code)
#     response = await call_next(request)
#     return response



# Define your secret key for JWT token
SECRET_KEY = "qwerty123456789"
ALGORITHM = "HS256"

# Password hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Authenticate user
def authenticate_user(username: str, password: str):
    db=get_db()
    db_user=get_user(db,username=username)   
    if not db_user or not pwd_context.verify(password,db_user.hashed_password):
        return False
    return db_user


#create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# Verify JWT token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    token:str    

# Token endpoint
@app.post("/login")
async def login_for_access_token(data:OAuth2PasswordRequestForm = Depends()):
    # username=data.get("username")
    # password=data.get("password")
    try:
        user = authenticate_user(data.username, data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        return str(e)    
    access_token_expires=timedelta(minutes=15)
    access_token = create_access_token(data={"sub": user.username, "role": user.role},
                                       expires_delta=access_token_expires)
    db=get_db()
    token=insert_token(db,id=user.id,token=access_token)
    return {"access_token": access_token, "token_type": "bearer"}



@app.get("/developer")
async def protected_route(token: str=Depends(oauth2_scheme)):
    decoded_token = decode_token(token)
    user_role = decoded_token.get("role")
    print("role",user_role)
    if user_role =='developer' or user_role=='admin':
        return {"message": "This is a protected route, only developer and admin users can access."}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions",
        )

@app.get("/admin")
async def protected_route(token: str=Depends(oauth2_scheme)):
    print(token)
    decoded_token = decode_token(token)
    user_role = decoded_token.get("role")
    if user_role == "admin":
        return {"message": "This is a protected route, only admin can users can access."}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions",
        )