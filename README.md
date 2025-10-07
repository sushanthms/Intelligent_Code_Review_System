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
intelligent-code-review-system/
│
├── backend/ # FastAPI backend
│ ├── app/
│ │ ├── main.py # FastAPI routes (API endpoints)
│ │ ├── analyzer.py # Python analysis logic (AST + runtime checks)
│ │ ├── schemas.py # Pydantic models for request/response
│ │ └── templates/ # JSON templates for explanations
│ ├── requirements.txt
│
├── frontend/ # React frontend
│ ├── src/
│ │ ├── App.jsx # Main app layout
│ │ ├── main.jsx # Entry point
│ │ ├── components/
│ │ │ ├── Editor.jsx # Code input area
│ │ │ └── Results.jsx # Analysis result display
│ ├── package.json
│ └── vite.config.js
│
└── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Backend (FastAPI)
Open a terminal in the **`backend`** folder:
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # On Windows
# or source venv/bin/activate  (Mac/Linux)

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

The backend will start at:
👉 http://127.0.0.1:8000

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

