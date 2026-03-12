# Finovo Platform

## Introduction
Finovo is a modern, feature-rich budget planner and financial tracking application. It is structured as a monorepo consisting of a backend API powered by Django and a mobile application built with React Native and Expo.

## Prerequisites
Ensure your system meets the following requirements before getting started:
- **Node.js** (v18+ recommended)
- **Python** (v3.10+ recommended)
- **Expo CLI** (Optional, installed globally via `npm install -g expo-cli`, but `npx expo` works fine)
- An iOS Simulator, Android Emulator, or the Expo Go app on a physical device for mobile development.

---

## Backend Setup (Django)

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows (Command Prompt / PowerShell):**
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Environment Configuration:**
   Create a `.env` file inside the `backend/` directory, mirroring your production or local configurations. Example:
   ```env
   SECRET_KEY=your_development_secret_key
   DEBUG=True
   ```
   *(Ensure `.env` is never committed to GitHub)*

6. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Start the Django development server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   The backend API will run on `http://localhost:8000`.

---

## 📱 Frontend Setup (React Native / Expo)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies:**
   ```bash
   npm install
   ```
   *(If you use Yarn, run `yarn install`)*

3. **Configure API Endpoints:**
   In your frontend code (typically located around `frontend/src/constants/api.js`), ensure your API base URL points to your backend. 
   - **Using an Emulator/Simulator:** Point to `http://10.0.2.2:8000` (Android) or `http://localhost:8000` (iOS).
   - **Using a Physical Device on Expo Go:** Point to your computer's local network IP address (e.g., `http://192.***.1.100:800`).

4. **Start the Expo development server:**
   ```bash
   npx expo start
   ```
---

## Usage Notes
- The Data Import/Export features depend thoroughly on `backend/media` remaining accessible and `openpyxl` operating correctly for XLSX parsing.
- For profile photos and avatars to map properly, your `MEDIA_URL` routes in Django must be correctly configured in conjunction with native device network configurations.
