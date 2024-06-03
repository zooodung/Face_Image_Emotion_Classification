from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import os
import sys
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import shutil
import json
import uuid
import tempfile
import asyncio
import logging
from fastapi import Form

# 현재 파일의 디렉토리 경로를 추가
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), 'web'))

from FEC_model_result import classificate_emotion
from API_text import generate_response, stt_function, talk_to_gpt, generate_first_response

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# CORS 설정 추가
origins = [
    "http://localhost",  # 또는 프론트엔드가 실행되는 실제 출처
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8088",
    "http://127.0.0.1:8088"  # 필요에 따라 추가
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
    name: str = "홍길동"
    introduce: str = "I'm Hong Kildong"
    emotions: List[UserEmotion] = []

user_data = UserProfile()
user_data.emotions = [
    #UserEmotion(year=2024, month=5, date=1, text="오늘은 기분이 좋다!", emotion="happy", aicharacter="Anna", aianswer = "TEST AI ANSWER", imageUrl = " "),
    #UserEmotion(year=2024, month=5, date=2, text="화가 난다!", emotion="anger", aicharacter="Anna", aianswer = "TEST AI ANSWER", imageUrl = " "),
    #UserEmotion(year=2024, month=5, date=3, text="슬프다...", emotion="sad", aicharacter="Anna", aianswer = "TEST AI ANSWER", imageUrl = " "),
]

# 사용자 로그인
@app.put("/user_login")
async def update_user_settings(user_custom: UserProfile):
  global user_data  # 전역 변수 사용 명시
  user_data = user_custom  # 설정 업데이트
  return {"message": "Create User successfully"}


class UserSettingsUpdate(BaseModel):
    a_attitude: str = "반말"
    intensity: float = 0.75 
    composition: List[str] = ["공감하기", "위로하기", "조언하기"] 
    length: int = 400      

default_setting = UserSettingsUpdate()

# prompt 사용자 세팅 put
@app.put("/user_settings")
async def update_user_settings(settings: UserSettingsUpdate):
  global default_setting  # 전역 변수 사용 명시
  default_setting = settings  # 설정 업데이트
  return {"message": "User settings updated successfully"}

# prompt 사용자 세팅 get
@app.get("/user_settings")
async def get_user_settings():
    return default_setting  # 현재 설정 반환


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
    a_attitude: str
    composition: List[str]
    intensity: float
    length: int
    name: str
    introduce: str

@app.post("/generate_response")
async def call_generate_response(data: RequestData):
    logging.info(f"Received data: {data}")
    text = data.text
    emotion = data.emotion
    a_attitude = data.a_attitude
    composition = data.composition
    intensity = data.intensity
    length = data.length
    name = data.name
    introduce = data.introduce

    response_text = generate_response(emotion, text, a_attitude, composition, intensity, length, name, introduce)
    return {"response": response_text}

# FastAPI 라우트 설정 (기존 app.py의 라우트를 FastAPI 형식으로 변경)
@app.post("/upload_chat_image")
async def upload_image(image: UploadFile = File(...)):
     # 이미지 저장
    file_name = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())
    
    emotion = classificate_emotion(file_path)
    response_text = generate_first_response(emotion)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, logger.info, f"Generated response_text: {response_text}")


    return {"response": response_text}

@app.post("/record_audio")
async def record_audio(audio: UploadFile = File(...)):
    global conversation_history  # 전역 변수 사용 명시
    
    # 임시 파일로 업로드된 오디오 파일 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        shutil.copyfileobj(audio.file, temp)
        temp_audio_path = temp.name  

    # temp_audio_path 파일이 존재하는지 확인
    if not os.path.exists(temp_audio_path):
        raise FileNotFoundError(f"Temp audio file not found: {temp_audio_path}")

    # STT 처리
    transcript = stt_function(temp_audio_path)
    
    # GPT-3와 대화
    gpt_response, conversation_history = talk_to_gpt(transcript, conversation_history)
    
    # 임시 파일 삭제
    os.remove(temp_audio_path)  

    logging.info(f"Generated response_text: {gpt_response}")

    return {"response": gpt_response}

# 정적 파일 라우팅 추가
app.mount("/", StaticFiles(directory="web", html=True), name="static")
app.mount("/images", StaticFiles(directory="web/images"), name="images")