# 🚀 Multi-Application RBAC API

A reusable, production-ready **Multi-Application RBAC Core API** built with **FastAPI**, **PostgreSQL**, and **Redis**.  
Designed to support **multiple applications**, **scoped permissions**, **audit logging**, and **high performance caching**.

---

## ✨ Key Features

- ✅ Multi-Application support (single core, multiple apps)
- ✅ Global User, Scoped Role & Permission per Application
- ✅ JWT Authentication (App-aware)
- ✅ Permission Cache with Redis
- ✅ Automatic Audit Logging (Middleware)
- ✅ Admin APIs (Role & Permission Management)
- ✅ Docker & Docker Compose ready
- ✅ Easily reusable for any backend system

---

## 🏗️ Architecture Overview

**Layered Architecture**
Client
↓
API Gateway / FastAPI
↓
Application Layer
├── Auth Service
├── RBAC Service
├── Audit Service
↓
Infrastructure Layer
├── PostgreSQL
├── Redis

---

## 🧩 Core Concepts

### 🔹 Multi-Application
One backend core can serve **multiple applications** using `app_code`.

### 🔹 RBAC Scoped by Application
- Same role name (`ADMIN`)  
- Different permissions per application  
- No role duplication required

### 🔹 Permission Cache
Permissions are cached in Redis per:
user_id + app_code

markdown

### 🔹 Audit Logging
- HTTP Request Logging (Middleware)
- Manual Audit for sensitive actions (Admin)

---

## 🗄️ Database Core Tables

- `tbl_user`
- `tbl_application`
- `tbl_user_application`
- `tbl_role`
- `tbl_permission`
- `tbl_user_role`
- `tbl_role_permission`
- `tbl_audit_log`
- `tbl_request_log`

---

## ⚙️ Environment Configuration

Copy `.env.example` to `.env`

```bash
cp .env.example .env
.env.example is for documentation
.env is for your local / server usage

🐳 Run with Docker
docker-compose build
docker-compose up -d
API will be available at:

Locahost
http://localhost:8000
Swagger:
http://localhost:8000/docs

🧪 Seed Initial Data
python app/core/seed.py

Creates:
DEFAULT_APP
SUPER_ADMIN role
Initial permissions
Admin user

🔐 Default Admin Account
Email    : admin@local.dev
Password : admin123

📦 Tech Stack
FastAPI
SQLAlchemy (Async)
PostgreSQL
Redis
JWT
Docker & Docker Compose

📄 License
MIT License

👨‍💻 Author
Built with ❤️ for reusable backend architecture
by Khairil Anwar