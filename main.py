import os
import json

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse

from router import router


app = FastAPI()

templates = Jinja2Templates(directory='./')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    
    # uvicorn을 사용하여 FastAPI 애플리케이션 실행
    uvicorn.run(app, host="0.0.0.0", port=8080)