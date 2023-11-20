from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path
from datetime import datetime

from phone_detection import ObjectDetector
from sleep_detection import DrowsinessDetector
import imutils
import cv2

fps = 10
result_phone = 0
MAX_IMAGES = 20

phone_detector = ObjectDetector()
sleep_detector = DrowsinessDetector(0.25, 20)

# 다른 서버의 API 엔드포인트
other_server_api_url = "/abnormal/detect"

router = APIRouter(
    responses={404: {"description": "Not found"}}
)

# 멀티파트 데이터를 받아오는 엔드포인트
@router.post(other_server_api_url)
async def get_image(
    file: UploadFile = File(...)
):
    try:
        # 멀티파트 데이터를 FormData로 변환
        data = {
            "file": (file.filename, file.file)
        }
        
        # 파일을 임시 디렉토리에 저장
        temp_dir = "/home/hagima-ml/ML-Server/AbnormalImgs"
        image_paths = []
        
        image_count = len(os.listdir(temp_dir))
        
        if image_count >= MAX_IMAGES:
            oldest_file = min(Path(temp_dir).iterdir(), key = os.path.getctime)
            os.remove(oldest_file)
            
        # timestamp를 활용하여 파일 저장
        timestamp = datetime.now().strftime("%y%m%d%H%M%S%f")[:-3]
        filename = f"{timestamp}.jpg"

        file_path = f"{temp_dir}/{filename}"
        
        with open(file_path, "wb") as dest:
            shutil.copyfileobj(file.file, dest)
        image_paths.append(file_path)

        ######################################민석수정#########################################   

        frame = cv2.imread(file_path, cv2.IMREAD_COLOR)
        #frame = imutils.resize(frame, width = 416)
        frame = imutils.resize(frame, width = 1024)

        result_phone = phone_detector.detect(frame)
        result_sleep = sleep_detector.detect_drowsiness(frame)
        print("driver sleeping: {}, driver phoning: {}".format(result_sleep, result_phone))

        ######################################################################################

        #process_image(file_path)

        # 얼굴 인식 결과에 따라 응답 처리            
        response_data = {"status": 200, "message": "사진 옴", "sleep": result_sleep, "phone": result_phone}
            
        return JSONResponse(content=response_data, status_code=200)
    
    except Exception as e:
        # 예외 처리: 에러 발생 시
        response_data = {"status": 500, "message": "사진 안 옴"}
        return JSONResponse(content=response_data, status_code=500)
