from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
import logging

from models import UserCreate, Token, User
from auth import create_access_token, get_password_hash, verify_password
from database import get_db

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)
):
    try:
        logger.info(f"Login attempt for user: {form_data.username}")
        cursor = db.cursor()
        cursor.execute(
            "SELECT username, password FROM users WHERE username = :username",
            {"username": form_data.username},
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        if not verify_password(form_data.password, user[1]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        access_token = create_access_token(data={"sub": user[0]})
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/signup", response_model=Token)
async def signup(user: UserCreate, db=Depends(get_db)):
    try:
        logger.info(f"Signup attempt for user: {user.username}")
        cursor = db.cursor()

        # Check if user exists
        cursor.execute(
            "SELECT username FROM users WHERE username = :username",
            {"username": user.username},
        )

        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        # Create new user
        hashed_password = get_password_hash(user.password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": user.username, "password": hashed_password},
        )
        db.commit()

        # Create access token
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
