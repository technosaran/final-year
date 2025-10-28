# AI Productivity Dashboard

A unified web dashboard that connects Gmail, Google Drive, and Calendar to provide productivity summaries, task insights, and daily performance analytics.

## 🚀 Features
- **Email Summary & Task Extraction**: Summarize Gmail messages and extract actionable tasks
- **Drive File Organizer**: Auto-tag and categorize Google Drive files using AI
- **Calendar Smart Overview**: Analyze meetings and suggest time optimization
- **Productivity Dashboard**: Clean UI showing daily insights and metrics

## 🛠️ Tech Stack (100% Free)
- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: Python FastAPI
- **AI**: Hugging Face Transformers (offline)
- **Database**: SQLite
- **APIs**: Google Gmail, Drive, Calendar
- **Auth**: Google OAuth 2.0
- **Hosting**: Render (backend) + Vercel (frontend)

## 📁 Project Structure
```
ai-productivity-dashboard/
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── App.jsx
│   └── package.json
└── README.md
```

## 🚀 Quick Start
1. Clone the repository
2. Set up Google OAuth credentials
3. Install backend dependencies: `pip install -r backend/requirements.txt`
4. Install frontend dependencies: `cd frontend && npm install`
5. Run backend: `uvicorn main:app --reload`
6. Run frontend: `npm run dev`

## 🔧 Setup Guide
See individual README files in backend/ and frontend/ directories for detailed setup instructions.