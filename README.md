# 💼 Sales Management System

A full-stack **Sales Management System** built with **FastAPI**, **Streamlit**, and **MySQL**, designed to manage users, products, orders, and analytics efficiently.  
The system provides **secure authentication**, **role-based access**, and a **real-time dashboard** for tracking sales and performance.

---

## 🚀 Overview

This project allows admins and users to manage sales data with proper access control and data validation.  
It demonstrates key backend and frontend integration concepts, authentication, and database consistency through triggers and constraints.

### 🔑 Key Features

- **JWT-based Authentication** — Secure login and session management  
- **Role-Based Access Control** — Separate permissions for admins and users  
- **Product & Order Management** — Add, edit, and view products, users, and transactions  
- **Real-Time Analytics Dashboard** — Search, sorting, and pagination for efficient data visualization  
- **Data Integrity Enforcement** — MySQL constraints, foreign keys, and triggers maintain consistency  

---

## 🧩 Tech Stack

| Layer | Technology |
|--------|-------------|
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **Database** | MySQL |
| **Authentication** | JWT Tokens |
| **Containerization** | Docker (optional) |

---

## ⚙️ Project Structure

```

sales-managment-system/
│
├── backend/
│   ├── main.py                # FastAPI entry point
│   ├── CRUD/                  # CRUD functions for (users, products, Category, orders, orderItem)
│   ├── routers/               # API routes (users, products, orders)
│   ├── models.py              # SQLAlchemy models
│   ├── database.py            # Database connection
│   ├── utils/                 # Helper functions (auth, hashing)
│
├── frontend/
│   ├── streamlit_app.py       # Streamlit UI
│   ├── components/            # UI elements
│
├── requirements.txt
└── README.md

````

---

## 🧠 Learning Objectives

- Integrating a Python web framework (FastAPI) with a database (MySQL)
- Building a secure and responsive Streamlit interface
- Managing authentication and authorization using JWT
- Designing database schemas with constraints and triggers
- Deploying a full-stack web app for public testing

---

## 🧪 How to Run Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/YamenMohamed/sales-managment-system.git
   cd sales-managment-system
``

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI backend**

   ```bash
   uvicorn backend.main:app --reload
   ```

4. **Run the Streamlit frontend**

   ```bash
   streamlit run frontend/streamlit_app.py
   ```

5. Access the app at:
   **Frontend:** [http://localhost:8501](http://localhost:8501)
   **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧱 Database Setup

* Import your SQL schema file or let SQLAlchemy create the tables automatically.
* Configure your database connection in `backend/database.py`, for example:

  ```python
  SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/sales_db"
  ```

---

## 🧑‍💻 Author

**Yamen Mohamed**
Fresh Computer Science Graduate | Backend & Full-Stack Developer
[GitHub](https://github.com/YamenMohamed)

---
