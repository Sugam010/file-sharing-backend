from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .. import models, schemas, auth, utils
from ..database import SessionLocal

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    encrypted = utils.encrypt_link(str(db_user.id))
    return {"message": "signup successful", "encrypted_link": encrypted}

@router.get("/verify")
def verify(encrypted: str, db: Session = Depends(get_db)):
    try:
        uid = utils.decrypt_link(encrypted)
        user = db.query(models.User).filter(models.User.id == int(uid)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_verified = True
        db.commit()
        return {"message": "email verified"}
    except:
        raise HTTPException(status_code=400, detail="Invalid link")

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"id": db_user.id})
    return {"access_token": token}

@router.get("/files")
def list_files(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = auth.decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    db_user = db.query(models.User).filter(models.User.id == user['id']).first()
    files = db.query(models.File).filter(models.File.user_id == db_user.id).all()
    return [schemas.FileOut.from_orm(f) for f in files]

@router.get("/download-file/{file_id}")
def get_download_link(file_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_data = auth.decode_token(token)
    db_user = db.query(models.User).filter(models.User.id == user_data['id']).first()
    if db_user.is_ops:
        raise HTTPException(status_code=403, detail="Only client users can download")
    encrypted = utils.encrypt_link(str(file_id))
    return {"download-link": f"/download/{encrypted}", "message": "success"}

@router.get("/download/{enc}")
def actual_download(enc: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    uid = auth.decode_token(token)
    user = db.query(models.User).filter(models.User.id == uid['id']).first()
    if user.is_ops:
        raise HTTPException(status_code=403, detail="Only client user allowed")
    file_id = utils.decrypt_link(enc)
    file = db.query(models.File).filter(models.File.id == int(file_id)).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return {"filepath": file.filepath, "filename": file.filename}