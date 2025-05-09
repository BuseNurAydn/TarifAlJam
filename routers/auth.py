from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import timedelta
from typing import Annotated
from pydantic import BaseModel, ValidationError
from models import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from services.auth_service import (
    get_password_hash,verify_password,
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
class UserCreate(BaseModel):
    email: str
    username: str
    firstName: str
    lastName: str
    role: str
    phone: str
    password: str
    confirmPassword: str

def get_db():  #Bu fonksiyon bize veritabanını veriyor
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/home")
def render_home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: db_dependency):
    # Kullanıcı adı ve email kontrolü
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Yeni kullanıcı oluştur
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        is_active=True,
        role="user"  # Varsayılan rol
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token":access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user(
        user_update: UserUpdate,
        db: db_dependency,
        current_user: User = Depends(get_current_active_user)
):
    # Kullanıcı bilgilerini güncelle
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "password" and value:
            setattr(current_user, "hashed_password", get_password_hash(value))
        elif field != "password":
            setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me")
async def delete_user(
        db: db_dependency,
        current_user: User = Depends(get_current_active_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Kayıt işlemi POST
@router.post("/register-form")
async def register_form(
    request: Request,
    db: db_dependency,
    email: str = Form(...),
    username: str = Form(...),
    firstName: str = Form(...),
    lastName: str = Form(...),
    role: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    confirmPassword: str = Form(...),
):
    # Form verilerini Pydantic modeline dönüştür
    try:
        user_data = UserCreate(
            email=email,
            username=username,
            firstName=firstName,
            lastName=lastName,
            role=role,
            phone=phone,
            password=password,
            confirmPassword=confirmPassword
        )
    except ValidationError as e:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Form verileri hatalı",
            "details": e.errors()
        })

    # Şifre kontrolü
    if password != confirmPassword:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Şifreler uyuşmuyor"
        })

    # Kullanıcı varlık kontrolü
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Kullanıcı adı veya email zaten kayıtlı"
        })

    # Yeni kullanıcı oluşturma
    new_user = User(
        email=email,
        username=username,
        first_name=firstName,
        last_name=lastName,
        phone_number=phone,
        hashed_password=get_password_hash(password),
        role=role or "user",
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Kayıt başarılı, login sayfasına yönlendir
    return RedirectResponse(url="/auth/login-page", status_code=303)