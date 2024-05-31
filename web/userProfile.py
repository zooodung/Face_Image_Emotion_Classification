from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import csv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

# 정적 파일 경로 설정
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

# ------------- 
# 서버에 class로 저장
class UserProfile(BaseModel):
    name: str
    introduce: str

@app.post("/submit")
def get_profile(name: str = Form(...), introduce: str = Form(...)):
    user_data = UserProfile(name=name, introduce=introduce)
    return user_data
# ------------

@app.get("/", response_class=HTMLResponse)
async def form_display(request: Request):
    return templates.TemplateResponse("/make_Profile.html", {"request": request})

@app.post("/submit")
async def handle_form(name: str = Form(...), introduce: str = Form(...)):
    # CSV 파일에 데이터 추가
    with open('userProfile.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, introduce])
    
    # main.html로 리디렉션
    # 수정 필요
    return RedirectResponse(url="/make_log.py", status_code=303)

# Uvicorn을 사용하여 서버 실행: `uvicorn userProfile:app --reload`
