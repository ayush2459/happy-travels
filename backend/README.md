# ✈️ Happy Travels

Multi-mode travel booking app — Flights, Trains, Buses, Cars with real Razorpay payments.

## Run Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # add your Razorpay keys
uvicorn app.main:app --reload --port 8000
```

## Run Frontend
```bash
cd frontend
npm install
npm run dev
```

## First time setup (existing DB)
```bash
cd backend
python migrate_db.py
```
