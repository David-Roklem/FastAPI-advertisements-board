import uvicorn

from fastapi import FastAPI

from core.config import settings
from api.users.user import router as user_router
from api.ads.ad import router as ads_router
from api.comments.comment import router as comments_router

app = FastAPI(title=settings.app_title)
app.include_router(user_router)
app.include_router(ads_router)
app.include_router(comments_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
