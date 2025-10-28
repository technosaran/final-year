import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Calendar, Clock, Users, TrendingUp, MapPin } from 'lucide-react'
import axios from 'axios'

const CalendarInsights = () => {
  const { getAuthHeaders } = useAuth()
  const [events, setEvents] = useState([])
  const [stats, setStats] = useState({})
  const [focusBlocks, setFocusBlocks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCalendarData()
  }, [])

  const fetchCalendarData = async () => {
    try {
      const headers = getAuthHeaders()
      
      const [eventsResponse, statsResponse, focusResponse] = await Promise.all([
        axios.get('/api/calendar/events', { headers }),
        axios.get('/api/calendar/stats', { headers }),
        axios.get('/api/calendar/focus-time', { headers })
      ])

      setEvents(eventsResponse.data.events || [])
      setStats(statsResponse.data)
      setFocusBlocks(focusResponse.data.focus_blocks || [])
    } catch (error) {
      console.error('Failed to fetch calendar data:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString([], {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    })
  }

  const getProductivityColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
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
          <h1 className="text-2xl font-bold text-gray-900">Calendar Insights</h1>
          <p className="text-gray-600">AI-powered schedule optimization and meeting analysis</p>
        </div>
        <button onClick={fetchCalendarData} className="btn-primary">
          Refresh
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center">
            <Calendar className="h-8 w-8 text-blue-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-600">Today's Meetings</p>
              <p className="text-2xl font-bold text-gray-900">{stats.today_meetings || 0}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-green-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-600">Weekly Average</p>
              <p className="text-2xl font-bold text-gray-900">
                {Math.round((stats.average_daily_meetings || 0) * 10) / 10}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className={`p-2 rounded-lg ${getProductivityColor(stats.productivity_score || 0)}`}>
              <TrendingUp className="h-6 w-6" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Productivity Score</p>
              <p className="text-2xl font-bold text-gray-900">{stats.productivity_score || 0}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Upcoming Events */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Events</h3>
        
        {events.length === 0 ? (
          <div className="text-center py-12">
            <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No upcoming events</h3>
            <p className="text-gray-600">Connect your Google Calendar to see AI insights</p>
          </div>
        ) : (
          <div className="space-y-4">
            {events.slice(0, 5).map((event) => (
              <div
                key={event.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
              >
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">{event.summary}</h4>
                  <div className="flex items-center text-sm text-gray-600 space-x-4 mt-1">
                    <div className="flex items-center">
                      <Clock className="h-4 w-4 mr-1" />
                      {formatDate(event.start)} at {formatTime(event.start)}
                    </div>
                    {event.attendees > 0 && (
                      <div className="flex items-center">
                        <Users className="h-4 w-4 mr-1" />
                        {event.attendees} attendees
                      </div>
                    )}
                    {event.location && (
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 mr-1" />
                        {event.location}
                      </div>
                    )}
                  </div>
                </div>
                
                {event.meeting_link && (
                  <a
                    href={event.meeting_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-secondary text-sm"
                  >
                    Join
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Focus Time Suggestions */}
      {focusBlocks.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Suggested Focus Time</h3>
          <div className="space-y-3">
            {focusBlocks.map((block, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-green-50 rounded-lg"
              >
                <div>
                  <p className="font-medium text-gray-900">
                    {formatTime(block.start)} - {formatTime(block.end)}
                  </p>
                  <p className="text-sm text-gray-600">{block.suggestion}</p>
                </div>
                <span className="text-sm font-medium text-green-600">
                  {Math.round(block.duration_hours * 10) / 10}h available
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Insights */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Insights</h3>
        <div className="space-y-3">
          {stats.insights?.map((insight, index) => (
            <div key={index} className="flex items-start">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-3 mt-2"></div>
              <p className="text-sm text-gray-700">{insight}</p>
            </div>
          )) || (
            <p className="text-sm text-gray-600">Connect your calendar to see personalized insights</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default CalendarInsights