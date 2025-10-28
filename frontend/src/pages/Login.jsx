import React, { useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Navigate, useSearchParams } from 'react-router-dom'
import { BarChart3, Mail, FolderOpen, Calendar, Zap } from 'lucide-react'

const Login = () => {
  const { login, handleAuthCallback, isAuthenticated, loading } = useAuth()
  const [searchParams] = useSearchParams()

  useEffect(() => {
    const code = searchParams.get('code')
    if (code) {
      handleAuthCallback(code)
        .then(() => {
          // Redirect will happen automatically via Navigate component
        })
        .catch((error) => {
          console.error('Auth callback error:', error)
        })
    }
  }, [searchParams, handleAuthCallback])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  const handleLogin = async () => {
    try {
      await login()
    } catch (error) {
      console.error('Login error:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center px-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="flex justify-center">
            <div className="flex items-center justify-center w-16 h-16 bg-primary-600 rounded-full">
              <BarChart3 className="h-8 w-8 text-white" />
            </div>
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            AI Productivity Dashboard
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Connect your Google services to get AI-powered productivity insights
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8 space-y-6">
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <Mail className="h-5 w-5 text-primary-600" />
              <span className="text-sm text-gray-700">Gmail summary & task extraction</span>
            </div>
            <div className="flex items-center space-x-3">
              <FolderOpen className="h-5 w-5 text-primary-600" />
              <span className="text-sm text-gray-700">Drive file organization</span>
            </div>
            <div className="flex items-center space-x-3">
              <Calendar className="h-5 w-5 text-primary-600" />
              <span className="text-sm text-gray-700">Calendar optimization insights</span>
            </div>
            <div className="flex items-center space-x-3">
              <Zap className="h-5 w-5 text-primary-600" />
              <span className="text-sm text-gray-700">AI-powered productivity analytics</span>
            </div>
          </div>

          <button
            onClick={handleLogin}
            className="w-full flex justify-center items-center px-4 py-3 border border-transparent text-sm font-medium rounded-lg text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
          >
            <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
              <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Continue with Google
          </button>

          <p className="text-xs text-gray-500 text-center">
            We'll only access your Gmail, Drive, and Calendar data to provide insights. 
            Your data is processed securely and never stored permanently.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login