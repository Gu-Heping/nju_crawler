"""
主应用入口：独立 FastAPI 爬虫服务

本文件将 crawler 作为主应用运行，支持直接启动。
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from crawler.router import router as crawler_router
from crawler.lifecycle import crawler_lifespan
from wechat.router import router as wechat_router
from wechat.lifecycle import wechat_lifespan
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def _combined_lifespan(app: FastAPI):
    # compose crawler and wechat lifespans so both background tasks run
    async with crawler_lifespan(app):
        async with wechat_lifespan(app):
            yield


app = FastAPI(lifespan=_combined_lifespan)
# Both crawler and wechat lifespans are now composed; routers mounted below
app.include_router(crawler_router)
app.include_router(wechat_router)

origins = [
    "*" 
    # 将来部署时, 您应该只允许您的前端网址
    # "http://your-frontend-domain.com", 
]

# 3. 添加中间件 (Middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 允许访问的来源
    allow_credentials=True,    # 允许 cookie
    allow_methods=["*"],       # 允许所有 HTTP 方法 (GET, POST, OPTIONS 等)
    allow_headers=["*"],       # 允许所有请求头
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
