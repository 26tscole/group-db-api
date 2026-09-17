from fastapi import FastAPI
from app.groups.routers.group_router import router as groups_router
from app.users.routers.users_router import router as users_router

app = FastAPI()

all_routers = [
    users_router,
    groups_router,
    # not implemented yet
    # app.debts.router.router,
    # app.activities.router.router,
]

for router in all_routers:
    app.include_router(router)
