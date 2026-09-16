from fastapi import FastAPI
from app.groups.router import router as groups_router

app = FastAPI()

all_routers = [
    groups_router,
    # not implemented yet
    # app.debts.router.router,
    # app.users.router.router,
    # app.activities.router.router,
]

for router in all_routers:
    app.include_router(router)
