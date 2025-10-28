# 🚀 AI Productivity Dashboard - Complete Setup Guide

This guide will walk you through setting up the complete AI Productivity Dashboard from scratch. Everything is **100% free** using open-source tools and free-tier services.

## 📋 Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Git installed
- Google account for OAuth setup

## 🏗️ Project Overview

**What you're building:**
- A unified dashboard connecting Gmail, Google Drive, and Calendar
- AI-powered email summarization and task extraction
- Intelligent file organization and categorization
- Calendar optimization and focus time suggestions
- Modern React frontend with real-time insights

**Tech Stack (All Free):**
- Frontend: React + Vite + Tailwind CSS
- Backend: Python FastAPI
- AI: Hugging Face Transformers (offline)
- Database: SQLite
- APIs: Google Gmail, Drive, Calendar
- Hosting: Render + Vercel (free tiers)

## 🔧 Step 1: Google Cloud Setup (5 minutes)

### 1.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "New Project" → Enter name: "AI Productivity Dashboard"
3. Click "Create"

### 1.2 Enable Required APIs
1. In the search bar, type "Gmail API" → Click "Enable"
2. Search "Google Drive API" → Click "Enable"  
3. Search "Google Calendar API" → Click "Enable"

### 1.3 Create OAuth Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: "AI Productivity Dashboard"
   - User support email: Your email
   - Developer contact: Your email
   - Save and continue through all steps
4. Create OAuth Client ID:
   - Application type: Web application
   - Name: "AI Dashboard Client"
   - Authorized redirect URIs: `http://localhost:8000/auth/callback`
5. **Save the Client ID and Client Secret** - you'll need these!

## 🐍 Step 2: Backend Setup (10 minutes)

### 2.1 Clone and Setup Backend
```bash
# Navigate to your project directory
cd ai-productivity-dashboard/backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your Google credentials
```

Edit `.env` file:
```env
GOOGLE_CLIENT_ID=your_client_id_from_step_1.3
GOOGLE_CLIENT_SECRET=your_client_secret_from_step_1.3
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
SECRET_KEY=your_random_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./productivity_dashboard.db
ENVIRONMENT=development
```

### 2.3 Start Backend Server
```bash
uvicorn main:app --reload
```

✅ **Backend should now be running at `http://localhost:8000`**

Test it: Open `http://localhost:8000/docs` to see the API documentation.

## ⚛️ Step 3: Frontend Setup (5 minutes)

### 3.1 Setup Frontend
```bash
# Open new terminal, navigate to frontend
cd ai-productivity-dashboard/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ **Frontend should now be running at `http://localhost:3000`**

## 🧪 Step 4: Test the Application (5 minutes)

### 4.1 Test Authentication Flow
1. Open `http://localhost:3000`
2. Click "Continue with Google"
3. Sign in with your Google account
4. Grant permissions for Gmail, Drive, and Calendar
5. You should be redirected back to the dashboard

### 4.2 Test Each Feature
1. **Dashboard**: Should show your stats (may be 0 initially)
2. **Email Summary**: Click to see recent emails with AI summaries
3. **Drive Organizer**: View your files categorized by AI
4. **Calendar Insights**: See your meetings and productivity score

## 🚀 Step 5: Free Deployment (Optional - 15 minutes)

### 5.1 Deploy Backend to Render
1. Push your code to GitHub
2. Go to [Render.com](https://render.com) → Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your repository
5. Configure:
   - Name: `ai-dashboard-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables from your `.env` file
6. Click "Create Web Service"

### 5.2 Deploy Frontend to Vercel
1. Go to [Vercel.com](https://vercel.com) → Sign up with GitHub
2. Click "New Project" → Import your repository
3. Configure:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add environment variable:
   - `VITE_API_BASE_URL`: Your Render backend URL
5. Click "Deploy"

### 5.3 Update OAuth Redirect
1. Go back to Google Cloud Console → Credentials
2. Edit your OAuth client
3. Add your Vercel URL to authorized redirect URIs:
   - `https://your-vercel-app.vercel.app/login`

## 🎯 Step 6: Customize and Extend

### 6.1 Customize AI Models
Edit `backend/services/ai_summary.py` to:
- Change summarization models
- Adjust task extraction patterns
- Modify file categorization rules

### 6.2 Add New Features
- Slack integration
- Notion API connection
- Email automation
- Custom productivity metrics

### 6.3 Improve UI
- Add dark mode
- Custom color themes
- Data visualization charts
- Mobile app with React Native

## 🐛 Troubleshooting

### Common Issues and Solutions

**1. OAuth Redirect Mismatch**
```
Error: redirect_uri_mismatch
```
**Solution**: Ensure the redirect URI in Google Console exactly matches your `.env` file.

**2. AI Models Not Loading**
```
Error: Failed to load AI models
```
**Solution**: Models download automatically on first run. Ensure internet connection and 2-3GB free space.

**3. CORS Errors**
```
Error: Access to fetch blocked by CORS policy
```
**Solution**: Ensure backend CORS is configured for your frontend URL in `main.py`.

**4. Token Expired**
```
Error: 401 Unauthorized
```
**Solution**: Refresh the page to get new tokens, or implement automatic token refresh.

**5. API Rate Limits**
```
Error: 429 Too Many Requests
```
**Solution**: Google APIs have daily quotas. Wait or implement caching to reduce requests.

## 📊 Usage Tips

### Maximizing Productivity Insights

1. **Email Management**:
   - Check email summaries daily
   - Use extracted tasks as your todo list
   - Archive processed emails

2. **File Organization**:
   - Review AI categorizations weekly
   - Create folders based on AI suggestions
   - Use consistent naming conventions

3. **Calendar Optimization**:
   - Block suggested focus time
   - Batch similar meetings
   - Aim for productivity score > 70

## 🔒 Security Best Practices

1. **Environment Variables**: Never commit `.env` files to git
2. **Token Storage**: Consider httpOnly cookies for production
3. **HTTPS**: Always use HTTPS in production
4. **Regular Updates**: Keep dependencies updated
5. **Access Control**: Limit OAuth scopes to minimum required

## 🎉 Congratulations!

You've successfully built a professional-grade AI Productivity Dashboard! This project demonstrates:

- ✅ Full-stack development (React + FastAPI)
- ✅ OAuth integration with Google APIs
- ✅ AI/ML integration with Hugging Face
- ✅ Modern UI/UX with Tailwind CSS
- ✅ Database management with SQLite
- ✅ Cloud deployment with free services

## 📚 Next Steps

1. **Portfolio**: Add this project to your GitHub and resume
2. **Blog**: Write about your experience building it
3. **Extend**: Add more integrations (Slack, Notion, etc.)
4. **Scale**: Implement Redis caching and PostgreSQL
5. **Mobile**: Build a React Native companion app

## 🤝 Contributing

Found a bug or want to add a feature? 
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

If you run into issues:
1. Check the troubleshooting section above
2. Review the individual README files in `/backend` and `/frontend`
3. Check Google Cloud Console for API quotas and errors
4. Ensure all environment variables are set correctly

**Happy coding! 🚀**