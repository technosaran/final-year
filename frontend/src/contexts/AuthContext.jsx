import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [accessToken, setAccessToken] = useState(localStorage.getItem('access_token'))

  useEffect(() => {
    // Check if user is already authenticated
    const token = localStorage.getItem('access_token')
    if (token) {
      setAccessToken(token)
      // You could validate the token here
      setUser({ authenticated: true })
    }
    setLoading(false)
  }, [])

  const login = async () => {
    try {
      const response = await axios.get('/auth/login')
      const { authorization_url } = response.data
      
      // Redirect to Google OAuth
      window.location.href = authorization_url
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  const handleAuthCallback = async (code) => {
    try {
      const response = await axios.get(`/auth/callback?code=${code}`)
      const { tokens } = response.data
      
      localStorage.setItem('access_token', tokens.access_token)
      if (tokens.refresh_token) {
        localStorage.setItem('refresh_token', tokens.refresh_token)
      }
      
      setAccessToken(tokens.access_token)
      setUser({ authenticated: true })
      
      return tokens
    } catch (error) {
      console.error('Auth callback failed:', error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setAccessToken(null)
    setUser(null)
  }

  const getAuthHeaders = () => {
    return accessToken ? { Authorization: `Bearer ${accessToken}` } : {}
  }

  const value = {
    user,
    loading,
    accessToken,
    login,
    logout,
    handleAuthCallback,
    getAuthHeaders,
    isAuthenticated: !!accessToken
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}