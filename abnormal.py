from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil

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
            "file": ("file.jpg", file.file)
        }
        
        # 파일을 임시 디렉토리에 저장
        temp_dir = "/home/hagima-ml/ML-Server/AbnormalImgs"
        image_paths = []
        for key, (filename, file) in data.items():
            file_path = f"{temp_dir}/{filename}"
            with open(file_path, "wb") as dest:
                shutil.copyfileobj(file, dest)
            image_paths.append(file_path)

        # 얼굴 인식 결과에 따라 응답 처리
        """ if deep_result in ("-1", "0", "1", "2", "3"):
            response_data = {"status": 200, "message": "얼굴 식별에 성공하였습니다.", "data": {"index": int(deep_result)}}
        else:
            response_data = {"status": 200, "message": "얼굴 식별에 실패하였습니다.", "data": {"index": -1}} """
            
        response_data = {"status": 200, "message": "사진 옴.", "data": {"index": 1}}
            
        return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        # 예외 처리: 에러 발생 시
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)