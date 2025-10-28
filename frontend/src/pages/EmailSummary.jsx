import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Mail, Clock, User, Tag } from 'lucide-react'
import axios from 'axios'

const EmailSummary = () => {
  const { getAuthHeaders } = useAuth()
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMessages()
  }, [])

  const fetchMessages = async () => {
    try {
      const headers = getAuthHeaders()
      const response = await axios.get('/api/gmail/messages', { headers })
      setMessages(response.data.messages || [])
    } catch (error) {
      console.error('Failed to fetch messages:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Email Summary</h1>
          <p className="text-gray-600">AI-powered email insights and task extraction</p>
        </div>
        <button onClick={fetchMessages} className="btn-primary">
          Refresh
        </button>
      </div>

      <div className="grid gap-6">
        {messages.length === 0 ? (
          <div className="card text-center py-12">
            <Mail className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No messages found</h3>
            <p className="text-gray-600">Connect your Gmail to see AI-powered summaries</p>
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className="card">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {message.subject}
                  </h3>
                  <div className="flex items-center text-sm text-gray-600 space-x-4">
                    <div className="flex items-center">
                      <User className="h-4 w-4 mr-1" />
                      {message.sender}
                    </div>
                    <div className="flex items-center">
                      <Clock className="h-4 w-4 mr-1" />
                      {new Date(message.date).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </div>

              <div className="mb-4">
                <h4 className="font-medium text-gray-900 mb-2">AI Summary</h4>
                <p className="text-gray-700 bg-gray-50 p-3 rounded-lg">
                  {message.summary || message.snippet}
                </p>
              </div>

              {message.tasks && message.tasks.length > 0 && (
                <div>
                  <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                    <Tag className="h-4 w-4 mr-2" />
                    Extracted Tasks
                  </h4>
                  <div className="space-y-2">
                    {message.tasks.map((task, index) => (
                      <div
                        key={index}
                        className="flex items-center p-2 bg-blue-50 rounded-lg"
                      >
                        <input
                          type="checkbox"
                          className="h-4 w-4 text-primary-600 rounded mr-3"
                        />
                        <span className="text-sm text-gray-700">{task}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default EmailSummary