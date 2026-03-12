from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.api.services.wg_service import get_server_public_key
from apps.api.db.session import get_db
from apps.api.models.user import User

router = APIRouter()


@router.post("/users")
def create_user(telegram_id: int, username: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if existing_user:
        return existing_user

    user = User(
        telegram_id=telegram_id,
        username=username,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/users/telegram/{telegram_id}")
def get_user_by_telegram_id(telegram_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/server-key")
def server_key():
    return {"server_public_key": get_server_public_key()}