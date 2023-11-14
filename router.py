from fastapi import APIRouter

from ml import router as ml_router
from abnormal import router as abnormal_router

# list of router
router = APIRouter()
router.include_router(ml_router, tags=["ml"])
router.include_router(abnormal_router, tags=["abnormal"])