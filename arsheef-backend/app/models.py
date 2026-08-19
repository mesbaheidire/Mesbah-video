"""
نماذج قاعدة البيانات (SQLAlchemy)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    linked_accounts = relationship("LinkedAccount", back_populates="owner")


class LinkedAccount(Base):
    """
    حساب منصة مرتبط بمستخدم — بعد نجاح OAuth
    هذا الجدول هو أساس التحقق من الملكية: أي طلب تنزيل
    يُقارَن بالحسابات الموجودة هنا فقط.
    """
    __tablename__ = "linked_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String, nullable=False)          # youtube / tiktok / instagram ...
    platform_account_id = Column(String, nullable=False)  # المعرف اللي ترجعه المنصة نفسها
    platform_username = Column(String, nullable=True)
    access_token = Column(String, nullable=False)       # يُفضَّل تشفيره قبل التخزين لاحقًا
    refresh_token = Column(String, nullable=True)
    is_verified = Column(Boolean, default=True)
    linked_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="linked_accounts")
