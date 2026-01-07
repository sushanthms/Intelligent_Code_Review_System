# 🧠 Intelligent Code Review System

 **Code review platform** that automatically analyzes Python code for **syntax errors**, **runtime issues**, and **code quality metrics** such as complexity, readability, and best practices.

This system helps developers get instant feedback on their code and understand how to improve it — similar to how a human reviewer would point out errors and provide suggestions.

## 🚀 Features

✅ **Automatic Code Review** — Detects syntax, runtime, and logic issues  
🧩 **Code Metrics** — Analyzes complexity, structure, and readability  
🧠 **Score-Based Evaluation** — Assigns a 0–100 score based on code quality  
💡 **Actionable Feedback** — Explains each issue with line numbers and fixes  
🎨 **Interactive Frontend** — Clean, responsive UI built with React and Tailwind CSS  
⚙️ **FastAPI Backend** — Handles code processing and analysis  
🔗 **Real-Time Communication** — Uses Axios to send code from frontend → backend  
📊 **Visual Results** — Displays issues, metrics, and improvement suggestions clearly  

## 🏗️ Project Structure
```
intelligent-code-review-system/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── analyze_python.py       # Code analysis logic (AST, runtime, scoring)
│   │   ├── templates/
│   │   │   └── explanation_templates.json
│   │   └── __pycache__/
│   │
│   ├── requirements.txt            # Python dependencies
│   
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main app layout
│   │   ├── main.jsx                # React root file
│   │   ├── components/
│   │   │   ├── Editor.jsx          # Code input editor
│   │   │   └── Results.jsx         # Displays analysis results
│   │   └── assets/                 # Optional icons/images
│   │
│   ├── package.json                # Frontend dependencies
│   ├── vite.config.js              # Vite config
│   ├── index.html                  # App HTML template
│   
│
├── README.md                       # Main project README
└── .gitignore                      # Ignore node_modules, venv, etc.
```
## ⚙️ Setup Instructions

## How to Run
1️⃣ Backend (FastAPI)
Open a terminal in the **`backend`** folder:
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # On Windows
# or source venv/bin/activate  (Mac/Linux)

pip install -r requirements.txt
To run the backend:
uvicorn app.main:app --reload --port 8000

## Common Errors & Fixes

During backend setup, the following issues may occur.

### uvicorn not found
Error message: uvicorn : The term 'uvicorn' is not recognized

**Solution:**
```bash
pip install uvicorn

fastapi not found

Error message: ModuleNotFoundError: No module named 'fastapi'
```bash
pip install fastapi
Running the Backend Server

After installing all required dependencies, start the backend server using:
```bash
uvicorn app.main:app --reload --port 8000
Alternative command (recommended on Windows):
```bash
python -m uvicorn app.main:app --reload --port 8000

2️⃣ **Frontend (React + Vite)**

Open a new terminal in the frontend folder:

cd frontend
npm install
npm run dev

The frontend will start at:
👉 http://localhost:5173

| Layer               | Technology                       | Purpose                            |
| ------------------- | -------------------------------- | ---------------------------------- |
| **Frontend**        | React.js + Tailwind CSS          | UI and user interactions           |
| **Backend**         | FastAPI (Python)                 | Core code analysis and API routes  |
| **Communication**   | Axios                            | Sends code from frontend → backend |
| **Code Analysis**   | Python AST, exec(), custom logic | Syntax & runtime analysis          |
| **Version Control** | Git + GitHub                     | Collaboration and presentation     |

