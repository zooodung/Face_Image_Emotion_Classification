import sys
import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi import Body
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import shutil
import json
import uuid
import tempfile

# 현재 파일의 디렉토리 경로를 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from FEC_model_result import classificate_emotion
from API_text import generate_response

app = FastAPI()

# CORS 설정 추가
origins = [
    "http://localhost",  # 또는 프론트엔드가 실행되는 실제 출처
    "http://localhost:8000",
    "http://127.0.0.1:8000"  # 필요에 따라 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 모델 정의 (UserEmotion, UserProfile)
class UserEmotion(BaseModel):
    year: int
    month: int
    date: int
    text: str
    emotion: str
    aicharacter: str
    aianswer: str 
    imageUrl: str 


class UserProfile(BaseModel):
    name: str
    introduce: str
    emotions: List[UserEmotion] = []

user_data = UserProfile(name="홍길동", introduce="I'm Hong Kildong")
user_data.emotions = [
    #UserEmotion(year=2024, month=5, date=1, text="오늘은 기분이 좋다!", emotion="happy", aicharacter="Anna", aianswer = "TEST AI ANSWER", imageUrl = " "),
    #UserEmotion(year=2024, month=5, date=2, text="화가 난다!", emotion="anger", aicharacter="Anna", aianswer = "TEST AI ANSWER", imageUrl = " "),
    #UserEmotion(year=2024, month=5, date=3, text="슬프다...", emotion="sad", aicharacter="Anna", aianswer = "TEST AI ANSWER", imageUrl = " "),
]

# 이미지 업로드 경로 설정
UPLOAD_DIR = "web/images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# API 엔드포인트

@app.get("/user")
def get_user():
    return user_data

@app.post("/user/emotions")
def add_emotion(emotion: UserEmotion):
    user_data.emotions.append(emotion)
    return {"message": "Emotion added successfully"}

@app.put("/user")
def update_user(new_user: UserProfile):
    global user_data
    user_data = new_user
    return {"message": "User updated successfully"}

#@app.post("/upload_image")
#async def upload_image(image: UploadFile = File(...)):
#    # 이미지 저장
#    file_name = f"{uuid.uuid4()}.jpg"
#    file_path = os.path.join(UPLOAD_DIR, file_name)
#    with open(file_path, "wb") as buffer:
#        buffer.write(await image.read())

#    return {"imageUrl": f"/images/{file_name}"}  # 이미지 URL 수정

#@app.post("/predict_emotion")
#async def predict_emotion(filename: str = Body(...)):
#    try:
#        file_path = os.path.join(UPLOAD_DIR, filename)

#        if not os.path.exists(file_path):
#            raise HTTPException(status_code=404, detail="File not found")

#        emotion = classificate_emotion(file_path)
#        return {"emotion": emotion}
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))
#// 계속 경로 에러 발생해서 이미지 저장할 때 동시에 감정 분류 실시함.

# 이미지 저장 및 감정 분류
@app.post("/upload_image")
async def upload_image(image: UploadFile = File(...)):
    # 이미지 저장
    file_name = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())
    
    emotion = classificate_emotion(file_path)

    return {"imageUrl": f"/images/{file_name}", "emotion": emotion}

# API 답변 생성
class RequestData(BaseModel):
    text: str
    emotion: str

@app.post("/generate_response")  # 엔드포인트 경로 확인
async def call_generate_response(data: RequestData):
    text = data.text
    emotion = data.emotion
    response_text = generate_response(emotion, text)
    return {"response": response_text}  # 반환 값 확인

# 정적 파일 라우팅 추가
app.mount("/", StaticFiles(directory="web", html=True), name="static")
app.mount("/images", StaticFiles(directory="web/images"), name="images")