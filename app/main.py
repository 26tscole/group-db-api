from fastapi import FastAPI
from app.groups.routers.group_router import router as group_router
from app.users.routers.users_router import router as users_router
from app.users.routers.platforms_router import router as platforms_router
from app.activities.routers.activity_router import router as activity_router
from app.activities.routers.activity_log_router import router as activity_log_router
from app.debts.routers.debts_router import router as debts_router

app = FastAPI()

all_routers = [
    users_router,
    platforms_router,
    group_router,
    activity_router,
    activity_log_router,
    debts_router,
]

for router in all_routers:
    app.include_router(router)
