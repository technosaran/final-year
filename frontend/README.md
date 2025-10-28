# AI Productivity Dashboard - Frontend

React frontend for the AI Productivity Dashboard with modern UI components and real-time data visualization.

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## 🛠️ Tech Stack

- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **Lucide React**: Beautiful icon library

## 📱 Features

### Dashboard
- Real-time productivity metrics
- Quick action buttons
- Daily insights and recommendations
- Activity timeline

### Email Summary
- AI-powered email summaries
- Automatic task extraction
- Sender and date information
- Interactive task checkboxes

### Drive Organizer
- File categorization with AI
- Visual category breakdown
- File size and modification date
- Direct links to Google Drive files

### Calendar Insights
- Meeting analysis and optimization
- Focus time suggestions
- Productivity scoring
- Upcoming events overview

## 🎨 UI Components

### Layout Components
- **Sidebar**: Navigation with active state indicators
- **Header**: Search bar, notifications, user menu
- **Layout**: Protected route wrapper with authentication

### Page Components
- **Dashboard**: Main overview with stats cards
- **EmailSummary**: Email list with AI insights
- **DriveOrganizer**: File management interface
- **CalendarInsights**: Calendar analytics dashboard

### Utility Components
- **AuthContext**: Authentication state management
- **Loading States**: Consistent loading indicators
- **Error Handling**: User-friendly error messages

## 🔧 Configuration

### Environment Variables
Create `.env.local` for custom configuration:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=AI Productivity Dashboard
```

### Proxy Configuration
Vite proxy is configured in `vite.config.js` to forward API calls to the backend:
```javascript
proxy: {
  '/api': 'http://localhost:8000',
  '/auth': 'http://localhost:8000'
}
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Layout.jsx       # Main layout wrapper
│   │   ├── Sidebar.jsx      # Navigation sidebar
│   │   └── Header.jsx       # Top header bar
│   ├── pages/               # Page components
│   │   ├── Dashboard.jsx    # Main dashboard
│   │   ├── Login.jsx        # Authentication page
│   │   ├── EmailSummary.jsx # Email insights
│   │   ├── DriveOrganizer.jsx # File management
│   │   └── CalendarInsights.jsx # Calendar analytics
│   ├── contexts/            # React contexts
│   │   └── AuthContext.jsx  # Authentication state
│   ├── App.jsx              # Main app component
│   ├── main.jsx             # React entry point
│   └── index.css            # Global styles
├── public/                  # Static assets
├── package.json             # Dependencies and scripts
└── vite.config.js           # Vite configuration
```

## 🎯 Key Features

### Authentication Flow
1. User clicks "Continue with Google"
2. Redirected to Google OAuth
3. Callback handled by AuthContext
4. Tokens stored in localStorage
5. Protected routes accessible

### Data Flow
1. Components use useAuth hook
2. API calls include authentication headers
3. Loading states during data fetch
4. Error handling for failed requests
5. Real-time data updates

### Responsive Design
- Mobile-first approach
- Tailwind CSS breakpoints
- Flexible grid layouts
- Touch-friendly interactions

## 🚀 Build and Deployment

### Production Build
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

### Deployment Options

1. **Vercel** (Recommended):
   ```bash
   npm install -g vercel
   vercel --prod
   ```

2. **Netlify**:
   - Connect GitHub repository
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **GitHub Pages**:
   - Use `gh-pages` package
   - Configure base URL in vite.config.js

## 🎨 Customization

### Tailwind Configuration
Modify `tailwind.config.js` for custom colors and themes:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        50: '#eff6ff',
        500: '#3b82f6',
        600: '#2563eb',
      }
    }
  }
}
```

### Component Styling
Use Tailwind utility classes and custom CSS components:
```css
@layer components {
  .card {
    @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6;
  }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure backend CORS is configured
   - Check proxy settings in vite.config.js

2. **Authentication Issues**:
   - Clear localStorage and retry
   - Check OAuth redirect URI configuration
   - Verify backend is running

3. **Build Errors**:
   - Clear node_modules and reinstall
   - Check for TypeScript errors
   - Verify all imports are correct

4. **Styling Issues**:
   - Ensure Tailwind CSS is properly configured
   - Check PostCSS configuration
   - Verify CSS imports

## 📊 Performance Optimization

- Code splitting with React.lazy()
- Image optimization
- Bundle analysis with `npm run build -- --analyze`
- Caching strategies for API calls
- Memoization for expensive computations

## 🔒 Security Considerations

- Tokens stored in localStorage (consider httpOnly cookies for production)
- Input validation and sanitization
- HTTPS in production
- Content Security Policy headers
- Regular dependency updates