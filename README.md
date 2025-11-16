SmartEyeCare – MVP Setup

Project structure

- backend: Flask API exposing prediction endpoints
- frontend: Next.js app with upload/webcam page

Prerequisites

**Option A: Using Nix (Recommended for MediaPipe support)**
- Nix package manager installed (https://nixos.org/download.html)
- Automatically provides Python 3.11 and all dependencies including MediaPipe

**Option B: Manual Setup**
- Python 3.10–3.11 recommended (3.13 may not support some ML libs)
- Node.js 18+ and npm
- MongoDB (local installation or MongoDB Atlas account)

Quick Start with Nix (Recommended)

**For users with Nix installed:**

1. Enter the Nix development environment:
   ```bash
   nix-shell
   # Or if using flakes:
   nix develop
   ```

2. This automatically:
   - Sets up Python 3.11 (MediaPipe compatible)
   - Installs all Python dependencies including MediaPipe
   - Sets up Node.js and npm
   - Installs frontend dependencies

3. Start the application:
   ```bash
   # From the Nix shell, run:
   npm start
   ```

The Nix environment ensures MediaPipe works correctly with Python 3.11, regardless of your system Python version.

---

Backend – run locally (Manual Setup)

1) MongoDB Setup:

   Option A - Local MongoDB:
   - Install MongoDB Community Server from https://www.mongodb.com/try/download/community
   - Start MongoDB service (usually runs automatically on Windows)
   - Default connection: mongodb://localhost:27017/

   Option B - MongoDB Atlas (Cloud):
   - Create free account at https://www.mongodb.com/cloud/atlas
   - Create a cluster and get connection string
   - Set environment variable: MONGODB_URI="your_atlas_connection_string"

2) Create and activate a virtual environment (Windows PowerShell):

   - python -m venv .venv
   - .\.venv\Scripts\Activate.ps1

3) Install dependencies:

   - pip install -r backend/requirements.txt

4) Start the API:

   - python backend/app.py

The API runs at http://localhost:5000

Database Configuration:

- Default database name: "smarteyecare"
- Users collection: stores email and hashed passwords
- Set environment variables to customize:
  - MONGODB_URI: MongoDB connection string (default: mongodb://localhost:27017/)
  - DATABASE_NAME: Database name (default: smarteyecare)

Environment Variables:

1. Copy the example environment file:
   ```bash
   cp backend/env.example .env
   ```

2. Edit `.env` file with your MongoDB connection details:
   - For local MongoDB: Use `mongodb://localhost:27017/`
   - For MongoDB Atlas: Use your Atlas connection string
   - Update `DATABASE_NAME` if needed (default: smarteyecare)

3. The backend will automatically read these environment variables

Health check:

- GET http://localhost:5000/api/health

API Endpoints:

Authentication:
- POST http://localhost:5000/signup (JSON: {email, password})
- POST http://localhost:5000/login (JSON: {email, password})

Prediction endpoints (MVP-friendly; work even without model files):
- POST http://localhost:5000/api/predict/redness (form-data: image=<file>)
- POST http://localhost:5000/api/predict/blink (form-data: video=<file>)
- POST http://localhost:5000/api/predict/myopia (form-data: image=<file>)

Frontend – run locally

1) Install dependencies:

   - cd frontend
   - npm install

2) Start the dev server:

   - npm run dev

The app runs at http://localhost:3000

Upload page:

- http://localhost:3000/upload

Notes

- For the MVP, the backend is resilient to missing model files and returns mock predictions where needed.
- To enable real predictions, place trained models in backend/models:
  - backend/models/redness_model.h5 (for redness detection)
  - backend/models/myopia_model.h5 (for myopia detection - optional)
- Blink detection uses MediaPipe (no model file needed - see below)

Blink Detection Setup:

Blink detection uses MediaPipe Face Mesh:

**Installation:**

**Option 1: Use Nix (Easiest - Recommended)**
The Nix development environment automatically provides Python 3.11 with MediaPipe:
```bash
nix-shell
# Or: nix develop
```

**Option 2: Manual Python 3.11 Setup (Current Setup)**
1. Python 3.11 virtual environment is already created at `backend/venv311/`
2. To activate it:
   ```bash
   backend\venv311\Scripts\Activate.ps1  # Windows PowerShell
   ```
3. Dependencies are installed. To reinstall:
   ```bash
   backend\venv311\Scripts\pip.exe install -r backend/requirements.txt
   backend\venv311\Scripts\pip.exe install mediapipe
   ```
4. To run the backend:
   ```bash
   backend\venv311\Scripts\python.exe backend/app.py
   ```

**Note:** If MediaPipe installation fails, blink detection will use fallback values. The rest of the application will work normally.

**How it works:**
- Uses MediaPipe Face Mesh to detect 468 facial landmarks
- Extracts eye landmark points from the face mesh
- Calculates Eye Aspect Ratio (EAR) for each frame
- Detects blinks when EAR drops below threshold
- Counts blinks and calculates blink rate (blinks per minute)
- Returns status: "low" (<12/min), "normal" (12-30/min), or "high" (>30/min)

**Advantages of MediaPipe:**
- ✅ No CMake or additional dependencies required
- ✅ Pre-trained models included (no separate download needed)
- ✅ Works on Windows, Linux, and macOS
- ✅ Fast and accurate face landmark detection
- ✅ Better performance than dlib in many cases

**Note:** If mediapipe is not installed, blink detection will return fallback values. The rest of the application will work normally.

Run both frontend and backend with one command

1) One-time setup at repo root:

   - npm run setup

2) Start both servers together (from repo root):

   - npm start

   This launches:
   - Backend at http://localhost:5000
   - Frontend at http://localhost:3000

Optional: ensure backend health before starting frontend:

- npm run start:wait

Troubleshooting setup (mediapipe / Python version)

- If npm run setup fails with “No matching distribution found for mediapipe”, it means your Python version isn’t supported by mediapipe. For the MVP, mediapipe is not required and has been removed from backend/requirements.txt.
- If you later add blink detection using mediapipe, use Python 3.10 or 3.11 and install:
  - pip install mediapipe==0.10.14
