# 🍽️ FastAPI Restaurant API

A simple FastAPI-based backend for managing restaurant menu items and customer orders, complete with PostgreSQL integration, logging, and testing.

---

## 🛠️ Setup (Using Docker)

### 1. Clone the repository
```bash
git clone https://github.com/muteeburrehman/fastapi_resturant_apis.git
cd restaurant-api
```

### 2. Create `.env` file
Copy the example and adjust credentials if needed:

```bash
cp .env.example .env
```

`.env.example` contents:
```bash
POSTGRES_USER=yourusername
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=yourdatabase
DATABASE_URL=postgresql://yourusername:yourpassword@localhost:5432/yourdatabase
```

Make sure this matches your `docker-compose.yml` and the environment inside the FastAPI app.

### 3. Build and Run the App
```bash
docker compose up --build
```

📍 The API will be available at: `http://localhost:8000`

## 📂 Project Structure

```
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── menu.py
│   │   └── order.py
├── tests/
│   ├── test_menu.py
│   └── test_order.py
├── orders_log.txt
├── docker-compose.yml
├── requirements.txt
├── .env
└── .gitignore
```

## 🧪 Run Tests
To run tests inside the container:
```bash
docker compose exec web pytest
```

## 🎯 API Usage (Examples with `curl`)

### ➕ Create Menu Item
```bash
curl -X POST http://localhost:8000/menu/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Pizza", "price": 12.99, "is_available": true}'
```

### 📋 List Available Menu Items
```bash
curl http://localhost:8000/menu/available/
```

### 🛒 Place an Order
```bash
curl -X POST http://localhost:8000/order/ \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Muteeb", "item_ids": [1]}'
```

### 📅 Get Today's Orders
```bash
curl http://localhost:8000/order/today/
```


## 🧬 Tech Stack
* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker
* Pytest

## 📎 Notes
* Orders are logged to `orders_log.txt`
* Uses `.env` file for DB config
* Swagger docs available at: 📄 http://localhost:8000/docs