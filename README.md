# Agent Bot Starter (Telegram + FastAPI + aiogram)

## 0) Talablar
- Python 3.11+
- Telegram bot token (@BotFather)
- (Keyinroq) HTTPS domen (webhook uchun), Google OAuth faqat Calendar modulini yoqsangiz kerak bo'ladi.

## 1) O'rnatish
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env   # va ichini to'ldiring
python init_db.py
```

`.env` ichida kamida `BOT_TOKEN` va `OPENAI_API_KEY` ni kiriting.
Agar lokal sinamoqchi bo'lsangiz `WEBHOOK_URL`ni bo'sh qoldiring.

## 2) Ishga tushirish (lokal, polling)
```bash
python run_polling.py
```
Bot xabarlarni polling orqali qabul qiladi (HTTPS kerak emas).

## 3) Webhook (serverda)
- Serverda HTTPS domen tayyor bo'lsa, `.env` dagi `WEBHOOK_URL`ga `https://<domen>/tg` yozing.
- Keyin:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
Bot avtomatik `set_webhook` qiladi.

## 4) Foydalanish
Telegram’da:
- `/start` — salomlashish
- **Tasks (Trello uslubida):**
  - `/tadd Matn ...` — task qo'shish (default: Today)
  - `/tlist` — ustunlar bo'yicha ko'rish (Today/Doing/Done)
  - `/tmove <id> <Column>` — ko'chirish
  - `/tdone <id>` — Done ga o'tkazish
- **Money:**
  - `/addexp <sum> "<izoh>" <kategoriya>` — xarajat
  - `/addin <sum> "<izoh>" <kategoriya>` — daromad
  - `/rep` — joriy oy hisobot (kategoriya kesimida)
- **Calendar (tayyor skeleton):**
  - `/link_calendar` — OAuth havola (placeholder)
  - `/calendar_on` — watch yoqish (placeholder)
  - `/calendar_test` — yaqin eventlarni ko'rish (placeholder)

> Calendar moduli stublar bilan keladi. Google OAuth sozlaganingizdan keyin `tools_calendar.py` ichidagi TODO’larni to'ldirasiz.

## 5) Agent Mode (OpenAI)
Bot javoblarni qisqa/aniq formatda berishi uchun `agent.py` dagi `SYSTEM_PROMPT` ishlatiladi. Tools orqali:
- task qo'shish/ro'yxat
- money qo'shish/hisobot
- (kelajakda) calendar eslatma pingi

## 6) Ma'lumotlar bazasi
Standart: SQLite `bot.db`. Keyin Postgres’ga o‘tkazish uchun `.env` dagi `DATABASE_URL`ni o‘zgartiring (masalan, `postgresql+psycopg2://user:pass@host/db`).

## 7) Google Calendar’ni yoqish (keyinchalik)
- Google Cloud’da OAuth Client (Web Application) yarating
- `.env`ga `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` kiriting
- `tools_calendar.py` dagi TODO’larni to‘ldiring, `/oauth/callback` endpointidan tokenni saqlang

---
## Agar "hammasini menga qilib ber" desangiz (agent mode)
Menga quyidagilarni yuboring:
1) Bot token (`BOT_TOKEN`)
2) Domen (HTTPS) yoki hosting kirishlari
3) Google OAuth Client (client_id/secret + redirect URL)
4) Qaysi DB: SQLite (oddiy) yoki Postgres (prod)
