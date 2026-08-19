from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import init_db, get_db
from app.models import User, LinkedAccount
from app.schemas import SignupRequest, LoginRequest, TokenResponse, LinkedAccountOut
from app.auth import hash_password, verify_password, create_access_token, decode_access_token
from app.config import settings

app = FastAPI(title="أرشيف API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@app.on_event("startup")
def on_startup():
    init_db()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="جلسة غير صالحة، سجّل الدخول مجددًا")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if user is None:
        raise HTTPException(status_code=401, detail="المستخدم غير موجود")
    return user


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/auth/signup", response_model=TokenResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجّل مسبقًا")

    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


@app.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="بيانات الدخول غير صحيحة")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


@app.get("/accounts/linked", response_model=list[LinkedAccountOut])
def list_linked_accounts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(LinkedAccount).filter(LinkedAccount.user_id == current_user.id).all()


@app.get("/oauth/{platform}/start")
def start_oauth(platform: str, current_user: User = Depends(get_current_user)):
    """
    نقطة بداية ربط منصة معينة.
    هذي حاليًا "هيكل" فقط — تحتاج نستبدلها برابط OAuth حقيقي
    من كل منصة (Google، TikTok for Developers...) بعد التسجيل كمطوّر عندهم
    والحصول على client_id الخاص بالمشروع.
    """
    supported = {"youtube", "tiktok", "instagram"}
    if platform not in supported:
        raise HTTPException(status_code=404, detail="المنصة غير مدعومة حاليًا")

    return {
        "message": f"هنا يتم توجيه المستخدم لصفحة تسجيل دخول {platform} الرسمية",
        "next_step": "استبدال هذه النقطة برابط OAuth حقيقي بعد الحصول على مفاتيح المطوّر"
    }
