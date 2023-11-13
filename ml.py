from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 다른 서버의 API 엔드포인트
other_server_api_url = "/member/recognition"

# 멀티파트 데이터를 받아오는 엔드포인트
@app.post(other_server_api_url)
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

        # 다른 서버로 POST 요청을 보냄
        response = subprocess.run(["python", "deep.py"], capture_output=True, text=True, input=str(data))

        # deep.py의 실행 결과 확인
        deep_result = response.stdout.strip()

        # 얼굴 인식 결과에 따라 응답 처리
        if deep_result in ("-1", "0", "1", "2", "3"):
            response_data = {"status": 200, "message": "얼굴 식별에 성공하였습니다.", "data": {"index": int(deep_result)}}
        else:
            response_data = {"status": 200, "message": "얼굴 식별에 실패하였습니다.", "data": {"index": -1}}
            
            return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        # 예외 처리: 에러 발생 시
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
    
if __name__ == "__main__":
    import uvicorn
    
    # uvicorn을 사용하여 FastAPI 애플리케이션 실행
    uvicorn.run(app, host="127.0.0.1", port=8080)
