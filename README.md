SmartEyeCare – MVP Setup

Project structure

- backend: Flask API exposing prediction endpoints
- frontend: Next.js app with upload/webcam page

Prerequisites

- Python 3.10–3.11 recommended (3.13 may not support some ML libs)
- Node.js 18+ and npm

Backend – run locally

1) Create and activate a virtual environment (Windows PowerShell):

   - python -m venv .venv
   - .\.venv\Scripts\Activate.ps1

2) Install dependencies:

   - pip install -r backend/requirements.txt

3) Start the API:

   - python backend/app.py

The API runs at http://localhost:5000

Health check:

- GET http://localhost:5000/api/health

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
  - backend/models/redness_model.h5
  - backend/models/blink_model.h5
  - backend/models/myopia_model.h5

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
