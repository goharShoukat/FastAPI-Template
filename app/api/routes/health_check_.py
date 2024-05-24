import core
from fastapi import APIRouter

router = APIRouter()


@router.get("/cero-risks-api", status_code=200)
async def health_check():
    try:
        core.initialise_postgres_session()
        return "Healthy Services"
    except Exception as e:
        raise e
