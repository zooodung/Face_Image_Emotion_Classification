from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    introduce = Column(String)

class UserEmotion(Base):
    __tablename__ = "user_emotions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    year = Column(Integer)
    month = Column(Integer)
    date = Column(Integer)
    text = Column(String)
    emotion = Column(String)
    aicharacter = Column(String)
    aianswer = Column(String, default="Test")
    imageUrl = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

class UserEmotionBase(BaseModel):
    year: int
    month: int
    date: int
    text: str
    emotion: str
    aicharacter: str
    aianswer: str = "Test"
    imageUrl: Optional[str] = None

class UserEmotionCreate(UserEmotionBase):
    pass

class UserEmotionResponse(UserEmotionBase):
    id: int

    class Config:
        orm_mode = True

class UserProfileBase(BaseModel):
    name: str
    introduce: str

class UserProfileCreate(UserProfileBase):
    username: str
    password: str

class UserProfileResponse(UserProfileBase):
    id: int
    emotions: List[UserEmotionResponse] = []

    class Config:
        orm_mode = True

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=dict)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/user", response_model=UserProfileResponse)
async def create_user(user: UserProfileCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        name=user.name,
        introduce=user.introduce
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/user", response_model=UserProfileResponse)
async def read_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_emotions = db.query(UserEmotion).filter(UserEmotion.user_id == current_user.id).all()
    return UserProfileResponse(
        id=current_user.id,
        name=current_user.name,
        introduce=current_user.introduce,
        emotions=user_emotions
    )

@app.post("/user/emotions", response_model=UserEmotionResponse)
async def add_emotion(emotion: UserEmotionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_emotion = UserEmotion(user_id=current_user.id, **emotion.dict())
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)
    return db_emotion

@app.post("/upload_image")
async def upload_image(image: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    file_name = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())
    return {"imageUrl": f"/images/{file_name}"}

app.mount("/", StaticFiles(directory="web", html=True), name="static")
app.mount("/images", StaticFiles(directory="web/images"), name="images")
