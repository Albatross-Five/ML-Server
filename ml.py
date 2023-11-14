from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil

from test_deepface import ImageVerifier

# 다른 서버의 API 엔드포인트
other_server_api_url = "/member/recognition"

router = APIRouter(
    responses={404: {"description": "Not found"}}
)

# 멀티파트 데이터를 받아오는 엔드포인트
@router.post(other_server_api_url)
async def recognize_faces(
    profile1: UploadFile = File(...),
    profile2: UploadFile = File(...),
    profile3: UploadFile = File(...),
    profile4: UploadFile = File(...),
    current: UploadFile = File(...)
):
    
    try:
        # 멀티파트 데이터를 FormData로 변환
        data = {
            "profile1": ("profile1.jpg", profile1.file),
            "profile2": ("profile2.jpg", profile2.file),
            "profile3": ("profile3.jpg", profile3.file),
            "profile4": ("profile4.jpg", profile4.file),
            "current": ("current.jpg", current.file),
        }

        # 파일을 임시 디렉토리에 저장
        temp_dir = "/home/hagima-ml/ML-Server/DeepfaceImgs"
        image_paths = []
        for key, (filename, file) in data.items():
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
            
        return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        # 예외 처리: 에러 발생 시
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
