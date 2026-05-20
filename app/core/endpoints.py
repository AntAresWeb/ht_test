from fastapi import APIRouter

from app.departments.endpoints import router as department_router
from app.employees.endpoints import router as employee_router

router = APIRouter()
router.include_router(department_router)
router.include_router(employee_router)
