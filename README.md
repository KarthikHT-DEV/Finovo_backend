# ⚙️ Finovo Backend API

This is the backend API for the **Finovo** budget planner application. It is built using **Django** and **Django REST Framework (DRF)**, providing a robust and secure foundation for financial data management, user authentication, and transaction processing.

## ✨ Features

- **User Authentication**: Secure signup and login using JWT (JSON Web Tokens).
- **Transaction API**: Full CRUD operations for tracking expenses and income.
- **Budget Management**: Backend logic for setting and monitoring financial goals.
- **Data Processing**: Support for importing and exporting financial data in Excel (XLSX) formats.
- **Media Handling**: Profile photo uploads and management.
- **Scalable Architecture**: Modular app structure (Users, Transactions, Core).

## 🛠️ Tech Stack

- **Framework**: [Django](https://www.djangoproject.com/)
- **API**: [Django REST Framework](https://www.django-rest-framework.org/)
- **Authentication**: SimpleJWT
- **Database**: PostgreSQL (via `psycopg2-binary`)
- **Environment Management**: `python-dotenv`
- **Excel Processing**: `openpyxl`
- **Image Handling**: `Pillow`

## 🚀 Getting Started

### Prerequisites

- **Python** (v3.10+)
- **PostgreSQL** (installed and running)
- **Virtual Environment** (recommended)

### Installation

1. **Navigate to the backend directory**:
   ```bash
   cd Finovo/backend
   ```

2. **Create and activate a virtual environment**:
   - **Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**:
   Create a `.env` file in the `backend/` directory with the following variables:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DB_NAME=finovo
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

### Database Setup

1. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

2. **(Optional) Seed the database**:
   ```bash
   python seed.py
   ```

## 🏃 Running the Server

Start the Django development server:

```bash
python manage.py runserver 0.0.0.0:8000
```
The API will be accessible at `http://localhost:8000`.

## 📁 Project Structure

```text
backend/
├── core/            # Project configuration and settings
├── users/           # User authentication and profile app
├── transactions/    # Financial transactions and logic app
├── media/           # User-uploaded files (profile photos, etc.)
├── requirements.txt # Python dependencies
├── manage.py        # Django management script
└── seed.py          # Database seeding script
```

## 🔐 API Documentation

Detailed API documentation is available via:
- **Redoc**: `http://localhost:8000/redoc/`
- **Swagger UI**: `http://localhost:8000/swagger/`
*(Ensure appropriate DRF documentation packages are enabled if needed)*

---
Developed as part of the Finovo Platform.
By Karthik Bisai - Developer(Hashtek Solutions Pvt.Ltd)
