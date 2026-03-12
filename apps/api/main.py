from fastapi import FastAPI

from apps.api.db.base import Base
from apps.api.db.session import engine

from apps.api.models.user import User
from apps.api.models.device import Device

from apps.api.routes.users import router as users_router
from apps.api.routes.devices import router as devices_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(devices_router)


@app.get("/")
def root():
    return {"message": "VPN Bot API running"}