from fastapi import FastAPI, Depends, HTTPException, status,Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from jose import JWTError
import jwt
from passlib.context import CryptContext
from typing import Optional
import models
import hashlib
import bcrypt
from database import engine
from crud import get_user
from sqlalchemy import text
from database import get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Define your secret key for JWT token
SECRET_KEY = "qwerty123456789"
ALGORITHM = "HS256"

# Password hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# OAuth2 scheme
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcmFuamFsaSIsInJvbGUiOiJkZXZlbG9wZXIifQ.vuVrPUQbxhYQoEqsJzrjXoOkPRRtdmRC8bUlHddjgjE")


# Authenticate user
def authenticate_user(username: str, password: str):
    db=get_db()
    db_user=get_user(db,username=username)
    hex_dig=pwd_context.encrypt(password)    
    if not db_user or not pwd_context.verify(password,db_user.hashed_password):
        return False
    return db_user


# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
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


# Token endpoint
@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/protected-route-developer")
async def protected_route(token: str):
    decoded_token = decode_token(token)
    user_role = decoded_token.get("role")
    if user_role =='developer' or user_role=='admin':
        return {"message": "This is a protected route, only developer and admin users can access."}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions",
        )

@app.post("/protected-route-admin")
async def protected_route(token: str):
    decoded_token = decode_token(token)
    user_role = decoded_token.get("role")
    if user_role == "admin":
        return {"message": "This is a protected route, only admin can users can access."}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions",
        )