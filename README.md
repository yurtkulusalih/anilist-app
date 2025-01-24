# anilist-app

## Docker

- You can simply start testing the application using docker:

```
docker compose up --build
```

- After that you can access the FE from `http://localhost:5173/`
- The API documentation can be accessed from `http://localhost:8000/docs`

## Local Setup

### Backend (FastAPI - Python 3.10)

1. Navigate under `backend/`

2. Create virtual environment and activate it:

```
python3 -m venv .venv

source .venv/bin/activate
```

3. Install dependencies using `requirements.txt`

```
pip install -r requirements.txt
```

4. Run tests

```
pytest tests/*
```

5. Start the application:

```
fastapi dev main.py
```

### Frontend (Vue3 - Node-20.18)

1. Navigate under `frontend/`

2. Install dependencies:

```
npm ci
```

3. Run the application:

```
npm run dev
```
