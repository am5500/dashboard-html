# DataBot - بوت تحليل البيانات

## هيكل المشروع

```
databot/
├── bot.py                  # نقطة البداية
├── server.py               # Flask لاستضافة الريبورتات
├── requirements.txt
├── .env.example
├── handlers/
│   ├── start_handler.py    # /start
│   ├── file_handler.py     # استقبال الملف
│   └── callback_handler.py # أزرار الاختيار
└── services/
    ├── analyzer.py         # التحليل عبر Claude API
    └── report_builder.py   # بناء HTML الداشبورد
```

## خطوات التشغيل

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. إعداد المتغيرات
```bash
cp .env.example .env
# عدل الـ .env وحط التوكنز
```

### 3. تشغيل السيرفر والبوت
```bash
# تيرمنال 1 - السيرفر
python server.py

# تيرمنال 2 - البوت
python bot.py
```

## المتغيرات المطلوبة

| المتغير | الوصف |
|---|---|
| `BOT_TOKEN` | من @BotFather على تيليجرام |
| `CLAUDE_API_KEY` | من console.anthropic.com |
| `BASE_URL` | عنوان السيرفر (IP:PORT) |

## الفلو

```
العميل يبعت CSV/Excel
    ↓
pandas يقرأ الملف
    ↓
أول 15 صف → Claude API
    ↓
Claude يرجع JSON (نوع الشارتس + الأعمدة + insights)
    ↓
Python يبني HTML داشبورد + plotly
    ↓
البوت يبعت رابط للعميل
```

## ملاحظات

- الريبورتات بتتحفظ في مجلد `reports/`
- الملفات المرفوعة في مجلد `downloads/`
- Claude بيشوف أول 15 صف فقط (توفير tokens)
- الشارتس تفاعلية كاملة (زوم + هوڤر + تحميل)
