from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.models.user import User
from app.utils import hash_password, verify_password
from app.schema.schema import UserCreate, LoginRequest, LoginResponse, UserInfo
import base64
from app.schema.schema import UserUpdate
from fastapi import Form, File, UploadFile
import os

router = APIRouter()


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        email=user_data.email,
        full_name=user_data.full_name
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="login or password is incorrect")

    # Create Base64 token: username:password
    raw_token = f"{data.username}:{data.password}"
    base64_token = base64.b64encode(raw_token.encode()).decode()

    # Photo URL ni bazadan olish
    photo_url = user.photo_url
    if photo_url:
        photo_url = os.path.join("uploads", os.path.basename(photo_url))    

    return {
        "message": "Login successful", 
        "token": base64_token, 
        "user": {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "photo_url": photo_url
        }
    }


@router.get("/logout")
def logout():
    return {"message": "Logged out"}




@router.patch("/update-profile")
def update_profile(
    username: str = Form(...),
    email: str = Form(None),  # None qilib qo'yish kerak
    full_name: str = Form(None),  # None qilib qo'yish kerak
    password: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Agar fayl yuklanmagan bo'lsa
        if not file:
            # Qismiy yangilash
            if email:
                user.email = email
            if full_name:
                user.full_name = full_name
            if password:
                user.hashed_password = hash_password(password)
            
            db.commit()
            
            return {
                "message": "Profile updated successfully",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "photo_url": f"uploads/{user.photo_url}" if user.photo_url else None
                }
            }

        # Agar fayl yuklangan bo'lsa
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Fayl nomini username bilan yaratish
        filename = user.username + "_" + file.filename
        file_path = os.path.join(upload_dir, filename)

        # Faylni saqlash
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # Qismiy yangilash
        if email:
            user.email = email
        if full_name:
            user.full_name = full_name
        if password:
            user.hashed_password = hash_password(password)
        user.photo_url = filename
        
        db.commit()
        
        return {
            "message": "Profile updated successfully",
            "user": {
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "photo_url": f"uploads/{filename}"
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

