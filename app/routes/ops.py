from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import models, schemas, auth, utils
from ..database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == payload.get("id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/ops/upload")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user.is_ops:
        raise HTTPException(status_code=403, detail="Only ops user can upload")
    if not utils.is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    path = utils.save_file(file)
    db_file = models.File(filename=file.filename, filepath=path, owner=current_user)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return {"message": "uploaded", "file_id": db_file.id}
