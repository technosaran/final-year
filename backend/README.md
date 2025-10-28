# AI Productivity Dashboard - Backend

FastAPI backend for the AI Productivity Dashboard that connects Gmail, Google Drive, and Calendar APIs with AI-powered insights.

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable APIs:
   - Gmail API
   - Google Drive API
   - Google Calendar API
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/auth/callback`
5. Download the credentials JSON file

### 3. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` with your Google OAuth credentials:
```env
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
SECRET_KEY=your_secret_key_here
```

### 4. Run the Server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Key Features

### Authentication
- Google OAuth 2.0 integration
- JWT token management
- Automatic token refresh

### Gmail Integration
- Fetch recent messages
- AI-powered email summarization
- Task extraction from email content
- Email statistics and insights

### Google Drive Integration
- File listing and categorization
- AI-powered file organization
- Storage analytics
- File type classification

### Google Calendar Integration
- Event fetching and analysis
- Meeting optimization suggestions
- Focus time recommendations
- Productivity scoring

### AI Services
- Offline text summarization using BART
- Task extraction with regex patterns
- File categorization
- Calendar efficiency analysis

## 🧠 AI Models Used

- **BART (facebook/bart-large-cnn)**: Email and text summarization
- **SentenceTransformers (all-MiniLM-L6-v2)**: Text classification and similarity
- **Custom algorithms**: Task extraction, calendar analysis

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── routes/              # API route handlers
│   ├── gmail.py         # Gmail API endpoints
│   ├── drive.py         # Google Drive endpoints
│   └── calendar.py      # Calendar API endpoints
├── services/            # Business logic services
│   ├── oauth_handler.py # OAuth authentication
│   └── ai_summary.py    # AI processing services
├── models/              # Database models and schemas
│   └── database.py      # SQLite database manager
└── requirements.txt     # Python dependencies
```

## 🔒 Security Notes

- OAuth tokens are stored securely
- API endpoints require authentication
- CORS configured for frontend integration
- Environment variables for sensitive data

## 🚀 Deployment

For production deployment:

1. **Render.com** (Recommended):
   - Connect your GitHub repository
   - Set environment variables in Render dashboard
   - Deploy automatically on git push

2. **Railway**:
   - Similar process to Render
   - Good free tier for small projects

3. **Heroku**:
   - Use `Procfile`: `web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}`
   - Set environment variables in Heroku dashboard

## 🐛 Troubleshooting

### Common Issues

1. **OAuth Redirect Mismatch**:
   - Ensure redirect URI in Google Console matches `.env` file
   - Check for trailing slashes

2. **AI Model Loading Errors**:
   - Models download automatically on first run
   - Ensure sufficient disk space (2-3GB for models)
   - Check internet connection for initial download

3. **API Rate Limits**:
   - Google APIs have daily quotas
   - Implement caching for production use
   - Consider upgrading to paid Google Cloud plan

4. **Token Expiration**:
   - Access tokens expire after 1 hour
   - Refresh tokens automatically handled
   - Check token refresh logic if issues persist

## 📊 Performance Tips

- Enable SQLite caching for API responses
- Use background tasks for heavy AI processing
- Implement pagination for large datasets
- Consider Redis for production caching