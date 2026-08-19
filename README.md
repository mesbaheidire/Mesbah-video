# أرشيف — Backend API

باك إند بسيط بـ FastAPI: تسجيل مستخدمين، تسجيل دخول (JWT)، وهيكل لربط حسابات المنصات عبر OAuth.

## التشغيل محليًا

```bash
cd backend
python -m venv venv
source venv/bin/activate      # على ويندوز: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

بعدها افتح: http://127.0.0.1:8000/docs — توثيق تفاعلي تلقائي لكل نقاط الـ API.

## النشر على Render

1. ارفع مجلد `backend` كامل إلى مستودع GitHub.
2. من لوحة Render: **New → Blueprint**، واختر المستودع — سيقرأ Render ملف `render.yaml` وينشئ الخدمة وقاعدة البيانات تلقائيًا.
3. أضف قيمة `FRONTEND_URL` يدويًا في إعدادات Environment (رابط موقعك الأمامي).
4. بعد أول نشر، جرّب: `https://اسم-مشروعك.onrender.com/health` — يفترض يرجع `{"status": "ok"}`.

## الخطوة الناقصة: OAuth حقيقي

نقطة `/oauth/{platform}/start` حاليًا هيكل فقط. لتفعيلها فعليًا لكل منصة تحتاج:

- **YouTube**: تسجيل مشروع في Google Cloud Console، تفعيل YouTube Data API، الحصول على `client_id` و`client_secret`.
- **TikTok**: التسجيل في TikTok for Developers، طلب صلاحيات الوصول المطلوبة (Login Kit).
- **Instagram**: التسجيل عبر Meta for Developers، إعداد تطبيق Instagram Basic Display أو Graph API.

كل منصة عندها مراجعة (App Review) قبل ما تسمح لك تستخدم صلاحيات حقيقية على حسابات مستخدمين غير حسابك أنت — هذا يستغرق وقت ويحتاج نوضح للمنصة إن الاستخدام مقتصر على أرشفة المستخدم لمحتواه الخاص.
