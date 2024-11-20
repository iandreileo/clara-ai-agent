from fastapi import APIRouter
from datetime import datetime
from app.core.utils.logging import logger, log_time

router = APIRouter()

@router.get("/")
@log_time
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

