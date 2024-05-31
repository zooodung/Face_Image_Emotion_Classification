from fastapi import FastAPI, Form, File, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv
import aiofiles
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

# 정적 파일 경로 설정
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
# app.mount("./web", StaticFiles(directory="web"), name="web")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_display(request: Request):
    return templates.TemplateResponse("make_log.html", {"request": request})

@app.post("/")
async def handle_form(year: int = Form(...), month: int = Form(...), date: int = Form(...), 
                      textInput: str = Form(...), imageInput: UploadFile = File(...)):
    # 이미지 저장 경로 설정
    img_directory = './img/'
    if not os.path.exists(img_directory):
        os.makedirs(img_directory)  # 디렉토리가 없으면 생성
    
    file_location = f"{img_directory}{imageInput.filename}"
    try:
        async with aiofiles.open(file_location, 'wb') as out_file:
            content = await imageInput.read()  # 이미지 파일 읽기
            await out_file.write(content)  # 이미지 파일 저장

        # CSV 파일에 데이터 추가
        with open('log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([1, year, month, date, textInput, file_location])
    except Exception as e:
        logger.error("Failed to write data: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Data saved successfully with image at {file_location}"}

# @app.get("/main")
# async def main_page():
#     return FileResponse('./web/main.html')

# Uvicorn을 사용하여 서버 실행: `uvicorn make_log:app --reload`
