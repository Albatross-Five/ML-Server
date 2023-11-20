from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from test_deepface import ImageVerifier

# 다른 서버의 API 엔드포인트
other_server_api_url = "/profile/recognition"

router = APIRouter(
    responses={404: {"description": "Not found"}}
)

# 멀티파트 데이터를 받아오는 엔드포인트
@router.post(other_server_api_url)
async def recognize_faces(
    profile1: UploadFile = File(None),
    profile2: UploadFile = File(None),
    profile3: UploadFile = File(None),
    profile4: UploadFile = File(None),
    current: UploadFile = File(None),
):
    
    try:
        # 멀티파트 데이터를 FormData로 변환
        data = {
            "profile1": ("profile1.jpg", profile1.file) if profile1 else None,
            "profile2": ("profile2.jpg", profile2.file) if profile2 else None,
            "profile3": ("profile3.jpg", profile3.file) if profile3 else None,
            "profile4": ("profile4.jpg", profile4.file) if profile4 else None,
            "current": ("current.jpg", current.file) if current else None,
        }
        
        data = {key: value for key, value in data.items() if value is not None}

        # 파일을 임시 디렉토리에 저장
        temp_dir = "/home/hagima-ml/ML-Server/DeepfaceImgs"
        image_paths = []
        for key, value in data.items():
            if value:
                filename, file = value
                file_path = f"{temp_dir}/{filename}"
                with open(file_path, "wb") as dest:
                    shutil.copyfileobj(file, dest)
                image_paths.append(file_path)

        verifier = ImageVerifier(image_paths)
        verification_results = verifier.verify_images()

        # 얼굴 인식 결과에 따라 응답 처리            
        # 성공
        min_index = verification_results.index(min(verification_results))
        response_data = {"status": 200, "message": "얼굴 식별에 성공하였습니다.", "data": {"index": int(min_index)}, "test": verification_results}
        
        for image_path in image_paths:
            os.remove(image_path)
        
        return JSONResponse(content=response_data, status_code=200)
    
    except Exception as e:
        # 예외 처리: 에러 발생 시
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
