from fastapi import FastAPI
from app.groups.routers.group_router import router as groups_router
from app.users.routers.users_router import router as users_router
from app.users.routers.platforms_router import router as platforms_router

app = FastAPI()

all_routers = [
    users_router,
    platforms_router,
    groups_router,
]

for router in all_routers:
    app.include_router(router)
