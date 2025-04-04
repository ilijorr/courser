from fastapi import APIRouter
from .endpoints import universities, courses

router = APIRouter(
        prefix="/v1",
        )

router.include_router(universities.router)
router.include_router(courses.router)
