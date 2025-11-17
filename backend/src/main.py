import asyncio

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth import router as auth_router
from src.config import settings
from src.database import check_db_connection, create_tables
from src.routers.group import router as group_router
from src.routers.student import router as student_router
from src.routers.user import router as user_router

app = FastAPI(
    title="Students API",
    description="API для учета успеваемости студентов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await asyncio.sleep(2)

    # Создаем таблицы при старте приложения
    await create_tables()
    # Проверяем подключение к БД
    if await check_db_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")

# Подключаем роутеры
main_router = APIRouter(prefix="/api")
main_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
main_router.include_router(user_router, tags=["Users"])
main_router.include_router(group_router, tags=["Groups"])
main_router.include_router(student_router, tags=["Students"])

app.include_router(main_router)


