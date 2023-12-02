import uvicorn

from fastapi import FastAPI

from core.config import settings
from api.users.user import router as user_router

app = FastAPI(title=settings.app_title)
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
