import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.groups.routers.group_router import router as group_router
from app.groups.routers.member_router import router as member_router
from app.users.routers.users_router import router as users_router
from app.users.routers.security_router import router as security_router
from app.connected_accounts.routers.platforms_router import router as platforms_router
from app.connected_accounts.routers.accounts_router import router as accounts_router
from app.activities.routers.activity_router import router as activity_router
from app.activities.routers.activity_log_router import router as activity_log_router
from app.debts.routers.debts_router import router as debts_router

app = FastAPI()

# Cookies require explicit origins (no "*") and allow_credentials=True
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

all_routers = [
    security_router,
    users_router,
    platforms_router,
    accounts_router,
    #group_router,
    #member_router,
    #activity_router,
    #activity_log_router,
    #debts_router,
]

for router in all_routers:
    app.include_router(router)
