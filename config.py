"""
إعدادات المشروع — تُقرأ من متغيرات البيئة (Environment Variables)
لا تكتب أي مفتاح سري هنا مباشرة، هذا فقط يقرأها من إعدادات Render.
"""
import os

class Settings:
    # رابط قاعدة البيانات (يوفره Render تلقائيًا عند ربط PostgreSQL)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./local_dev.db")

    # سر توقيع الجلسات/التوكنات (JWT) — يُولَّد عشوائيًا في الإنتاج
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # بيانات OAuth لكل منصة — تُضاف لاحقًا عند التسجيل كمطوّر في كل منصة
    YOUTUBE_CLIENT_ID: str = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET: str = os.getenv("YOUTUBE_CLIENT_SECRET", "")

    TIKTOK_CLIENT_KEY: str = os.getenv("TIKTOK_CLIENT_KEY", "")
    TIKTOK_CLIENT_SECRET: str = os.getenv("TIKTOK_CLIENT_SECRET", "")

    # عنوان الواجهة الأمامية (للسماح بطلبات CORS منها فقط)
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

settings = Settings()
