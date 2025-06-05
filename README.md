# Asynchronous Python CRUD API 
A simple CRUD API created using FastAPI, that leverages asynchronous execution to improve maximum number of concurrent requests, reducing latency and CPU load! Asynchronous APIs can drastically improve performance of application, especially IO bound 
applications. 

### Requirements: 
- Python
- FastAPI 
- Postgres
- SQLAlchemy (asyncio)

## Setup: 
**1. Clone:**  
```
git clone https://github.com/adi-tyasingh/fast-api.git
```

**2. Setup Postgres container:**
```
chmod +x ./scripts/postgre.sh
bash ./scripts/postgre.sh
```

**3. Start application: **
```
fastapi dev main.py
```
